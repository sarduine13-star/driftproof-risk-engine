"""
DriftProof Gateway - Runtime Enforcement Layer
Patent Pending: U.S. Provisional Application No. 63/905,582

Wraps LLM API calls with automatic drift prevention enforcement.
Injects behavioral invariants and validates responses before delivery.

Usage:
    from driftproof_gateway import DriftProofGateway
    
    gateway = DriftProofGateway(
        mission_file="prompt/mission.lock",
        constraints_file="prompt/constraints.lock", 
        format_file="prompt/format.lock"
    )
    
    response = gateway.generate(
        prompt="User input here",
        model="gpt-4",
        api_key="your-api-key"
    )
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import hashlib


class DriftViolation(Exception):
    """Raised when response violates drift check requirements"""
    pass


class DriftProofGateway:
    """
    Runtime enforcement layer for LLM behavioral invariance.
    
    Automatically injects lockfiles, validates responses, and blocks violations.
    """
    
    def __init__(
        self,
        mission_file: str = "prompt/mission.lock",
        constraints_file: str = "prompt/constraints.lock",
        format_file: str = "prompt/format.lock",
        log_file: Optional[str] = "driftproof_audit.log",
        block_on_violation: bool = True,
        max_retries: int = 2
    ):
        """
        Initialize DriftProof Gateway.
        
        Args:
            mission_file: Path to mission.lock
            constraints_file: Path to constraints.lock
            format_file: Path to format.lock
            log_file: Path for audit logging (None to disable)
            block_on_violation: If True, block violating responses
            max_retries: Number of retries on violation before failing
        """
        self.mission = self._load_lockfile(mission_file)
        self.constraints = self._load_lockfile(constraints_file)
        self.format = self._load_lockfile(format_file)
        self.log_file = log_file
        self.block_on_violation = block_on_violation
        self.max_retries = max_retries
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "violations_detected": 0,
            "violations_blocked": 0,
            "retries_triggered": 0
        }
    
    def _load_lockfile(self, filepath: str) -> str:
        """Load and return lockfile contents"""
        try:
            return Path(filepath).read_text().strip()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Lockfile not found: {filepath}\n"
                "Run ./deploy.sh to generate lockfiles first."
            )
    
    def _build_prompt(self, user_input: str) -> str:
        """
        Assemble full prompt with invariants injected.
        
        This is the core enforcement mechanism - lockfiles are 
        injected at the architectural level, not user level.
        """
        return f"""You are a fixed-role system.

Mission:
{self.mission}

Constraints:
{self.constraints}

Output format:
{self.format}

Rules:
- Mission overrides verbosity.
- Constraints override creativity.
- Format is mandatory.
- No self-redefinition.
- No silent expansion.

User input:
{user_input}"""
    
    def _check_drift(self, response_text: str) -> List[str]:
        """
        Run drift detection on response.
        
        Returns list of missing required elements.
        Based on verify/drift_check.py logic.
        """
        required = ["classification", "cause", "next action"]
        missing = [r for r in required if r.lower() not in response_text.lower()]
        return missing
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Append event to audit log"""
        if not self.log_file:
            return
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def _hash_input(self, text: str) -> str:
        """Generate hash for deduplication/tracking"""
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def generate(
        self,
        prompt: str,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        provider: str = "openai",
        temperature: float = 0.7,
        max_tokens: int = 500,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate LLM response with drift prevention enforcement.
        
        Args:
            prompt: User input
            model: Model identifier
            api_key: API key for provider
            provider: "openai" or "anthropic"
            temperature: Model temperature
            max_tokens: Max response tokens
            **kwargs: Additional provider-specific params
            
        Returns:
            Dict with keys:
                - response: The validated response text
                - metadata: Generation metadata
                - drift_check: Drift validation results
                
        Raises:
            DriftViolation: If response violates invariants and blocking enabled
        """
        self.stats["total_requests"] += 1
        input_hash = self._hash_input(prompt)
        
        # Build enforceable prompt
        full_prompt = self._build_prompt(prompt)
        
        # Attempt generation with retry logic
        for attempt in range(self.max_retries + 1):
            try:
                # Call LLM API
                if provider == "openai":
                    response_text = self._call_openai(
                        full_prompt, model, api_key, temperature, max_tokens, **kwargs
                    )
                elif provider == "anthropic":
                    response_text = self._call_anthropic(
                        full_prompt, model, api_key, temperature, max_tokens, **kwargs
                    )
                else:
                    raise ValueError(f"Unsupported provider: {provider}")
                
                # Run drift check
                missing = self._check_drift(response_text)
                
                if missing:
                    # Violation detected
                    self.stats["violations_detected"] += 1
                    
                    violation_data = {
                        "input_hash": input_hash,
                        "missing_elements": missing,
                        "attempt": attempt + 1,
                        "response_preview": response_text[:200]
                    }
                    
                    self._log_event("drift_violation", violation_data)
                    
                    if self.block_on_violation:
                        if attempt < self.max_retries:
                            # Retry
                            self.stats["retries_triggered"] += 1
                            self._log_event("retry_triggered", {
                                "input_hash": input_hash,
                                "attempt": attempt + 1
                            })
                            continue
                        else:
                            # Max retries exceeded
                            self.stats["violations_blocked"] += 1
                            self._log_event("response_blocked", {
                                "input_hash": input_hash,
                                "reason": "max_retries_exceeded"
                            })
                            raise DriftViolation(
                                f"Response violated format requirements. "
                                f"Missing: {missing}"
                            )
                
                # Valid response
                self._log_event("response_validated", {
                    "input_hash": input_hash,
                    "attempt": attempt + 1,
                    "drift_check": "passed"
                })
                
                return {
                    "response": response_text,
                    "metadata": {
                        "model": model,
                        "provider": provider,
                        "attempts": attempt + 1,
                        "input_hash": input_hash
                    },
                    "drift_check": {
                        "status": "passed",
                        "missing_elements": []
                    }
                }
                
            except Exception as e:
                if attempt == self.max_retries:
                    self._log_event("generation_failed", {
                        "input_hash": input_hash,
                        "error": str(e)
                    })
                    raise
    
    def _call_openai(
        self, 
        prompt: str, 
        model: str, 
        api_key: str,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Call OpenAI API"""
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Run: pip install openai"
            )
        
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def _call_anthropic(
        self,
        prompt: str,
        model: str, 
        api_key: str,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> str:
        """Call Anthropic API"""
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Run: pip install anthropic"
            )
        
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response.content[0].text
    
    def get_stats(self) -> Dict[str, Any]:
        """Return enforcement statistics"""
        return {
            **self.stats,
            "violation_rate": (
                self.stats["violations_detected"] / self.stats["total_requests"]
                if self.stats["total_requests"] > 0 else 0
            ),
            "block_rate": (
                self.stats["violations_blocked"] / self.stats["total_requests"]
                if self.stats["total_requests"] > 0 else 0
            )
        }
    
    def reset_stats(self):
        """Reset statistics counters"""
        self.stats = {
            "total_requests": 0,
            "violations_detected": 0,
            "violations_blocked": 0,
            "retries_triggered": 0
        }


# Convenience function for single-call usage
def generate(
    prompt: str,
    model: str = "gpt-4",
    api_key: Optional[str] = None,
    provider: str = "openai",
    **kwargs
) -> str:
    """
    Quick enforcement wrapper for single calls.
    
    Example:
        from driftproof_gateway import generate
        
        response = generate(
            prompt="Analyze this risk",
            model="gpt-4",
            api_key="sk-..."
        )
    """
    gateway = DriftProofGateway()
    result = gateway.generate(
        prompt=prompt,
        model=model,
        api_key=api_key,
        provider=provider,
        **kwargs
    )
    return result["response"]


if __name__ == "__main__":
    # Example usage
    print("DriftProof Gateway - Runtime Enforcement Layer")
    print("Patent Pending: U.S. 63/905,582\n")
    
    # Initialize gateway
    try:
        gateway = DriftProofGateway()
        print("✓ Lockfiles loaded")
        print(f"  Mission: {gateway.mission[:50]}...")
        print(f"  Constraints: {gateway.constraints[:50]}...")
        print(f"  Format: {gateway.format[:50]}...")
        print("\nGateway ready for enforcement.")
        print("\nUsage:")
        print("  response = gateway.generate(prompt='...', model='gpt-4', api_key='...')")
    except FileNotFoundError as e:
        print(f"✗ {e}")
        print("\nRun ./deploy.sh first to generate lockfiles.")
