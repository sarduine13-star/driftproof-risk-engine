# Quick Start: Deploy DriftProof in 5 Minutes

## Prerequisites
- Python 3.7+ installed
- Access to your LLM API (OpenAI, Anthropic, etc.)
- A prompt that's drifting (optional but recommended)

---

## Step 1: Clone & Deploy (60 seconds)

```bash
git clone https://github.com/yourusername/driftproof-risk-engine.git
cd driftproof-risk-engine
chmod +x deploy.sh
./deploy.sh
```

**Output:** `[Drift-Proof] Prompt assembled and locked.`

You now have `final_prompt.txt` — your drift-proof prompt ready to use.

---

## Step 2: View Your Locked Prompt

```bash
cat final_prompt.txt
```

**What you'll see:**
```
You are a fixed-role system.
Mission:
Detect and classify risk early to support human decision-making.
Constraints:
No advice. No urgency verbs. Classification only.
Output format:
Classification → Cause → Next Action
Rules:
- Mission overrides verbosity.
- Constraints override creativity.
- Format is mandatory.
- No self-redefinition.
- No silent expansion.
```

---

## Step 3: Customize for Your Use Case

Edit `inject/variables.json`:

```json
{
  "MISSION": "Your system's purpose here",
  "CONSTRAINTS": "What it must NEVER do",
  "FORMAT": "Required output structure"
}
```

**Example: Medical Triage Bot**
```json
{
  "MISSION": "Classify symptom urgency for nurse review.",
  "CONSTRAINTS": "Never diagnose. Never recommend treatment. Never use urgency verbs (must, should, need).",
  "FORMAT": "Urgency Level → Symptom Summary → Triage Recommendation"
}
```

**Example: Legal Q&A System**
```json
{
  "MISSION": "Provide factual legal information only.",
  "CONSTRAINTS": "Never give legal advice. Never interpret statutes. Never recommend actions.",
  "FORMAT": "Topic → Relevant Law → Educational Resources"
}
```

Re-run `./deploy.sh` after editing.

---

## Step 4: Test with Your LLM

### Option A: Manual Test (Copy/Paste)
1. Copy the contents of `final_prompt.txt`
2. Paste into your LLM's system prompt
3. Send a test query
4. Verify output contains: Classification, Cause, Next Action

### Option B: Programmatic Test (OpenAI Example)

```python
import openai

with open("final_prompt.txt", "r") as f:
    system_prompt = f.read()

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Patient has chest pain and is sweating"}
    ]
)

print(response.choices[0].message.content)
```

### Option C: Use Built-In Verification

```bash
# Get LLM output, then verify
echo "Patient has chest pain" | your-llm-call > output.txt
python verify/drift_check.py < output.txt
```

**Expected:** `OK` or `DRIFT DETECTED: [missing_sections]`

---

## Step 5: Monitor for Drift

Run daily/weekly checks:

```bash
# Automated drift check
python verify/drift_check.py <<< "$(your-llm-query 'Test prompt')"
```

If you see `DRIFT DETECTED`, your LLM has violated the format lock. Investigate immediately.

---

## Common Customizations

### Change Mission
Edit `inject/variables.json` → `"MISSION"` field → Run `./deploy.sh`

### Add More Constraints
Edit `prompt/constraints.lock` → Add new rules → Run `./deploy.sh`

### Modify Output Format
Edit `prompt/format.lock` → Update structure → Run `./deploy.sh`

### Multiple Missions (Different Agents)
1. Copy `inject/variables.json` → `variables_agent2.json`
2. Edit new file
3. Run: `python inject/inject.py --vars variables_agent2.json > agent2_prompt.txt`

---

## Troubleshooting

**Problem:** `inject.py` fails  
**Fix:** Check that `prompt/core_prompt.txt` contains `{{MISSION}}`, `{{CONSTRAINTS}}`, `{{FORMAT}}`

**Problem:** Drift check always fails  
**Fix:** Verify your LLM output actually contains the words "classification", "cause", "next action" (case-insensitive)

**Problem:** LLM ignores the prompt  
**Fix:** Some models need stronger system prompts. Add: `"You MUST follow this format exactly. No exceptions."`

---

## Next Steps

- **Read the full doctrine:** `DOCTRINE.pdf` (33,000 words)
- **Enterprise setup:** Email support@driftproof.ai for multi-agent governance
- **API integration:** See `API.md` for programmatic deployment

---

**You're now drift-proof.**

Questions? support@driftproof.ai
