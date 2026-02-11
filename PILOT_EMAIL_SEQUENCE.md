# F500 Pilot Email Sequence

---

## Day 1: Cold Outreach (LinkedIn DM or Email)

**Subject:** Deployable LLM guardrail. 60s setup. [FirstName]

---

Hi [FirstName],

Saw [Company] is deploying LLM agents for [use case — customer support/compliance/internal tools].

Quick question: Have you dealt with prompt drift yet?

(That thing where your agent gradually reinterprets its mission — like a support bot that starts making policy promises, or a triage system that starts diagnosing.)

We built an architectural fix. Not monitoring. Not RAG. Just structural impossibility.

**60-second deploy. Works Day 1. No ML required.**

Worth a 15-min demo this week?

— Stephen  
DriftProof Risk Engine  
[GitHub link]

---

**Response to "tell me more":**

It's a lockfile system for LLM prompts.

Think of it like this:
- Your agent has a mission (e.g., "classify symptom urgency")
- Traditional approach: hope it stays on mission
- DriftProof: architectural constraints that make deviation impossible

Six behavioral invariants:
1. Identity Lock (never forgets what it is)
2. Mission Lock (purpose cannot shift)
3. Constraint Cage (hard boundaries)
4. Format Lock (output structure enforced)
5. Interpretive Invariance (filters context, doesn't absorb it)
6. Operator Invariance (your sovereignty, not the user's)

I can show you on your actual prompts. 15 min this week?

---

## Day 2: Demo Setup Email

**Subject:** Demo setup: DriftProof on your prompts

---

Hi [FirstName],

For tomorrow's call, send me:
1. Your worst-behaving agent prompt (the one that drifts)
2. Example of a "good" vs "bad" output
3. What you've tried so far (prompt tweaks, monitoring, etc.)

I'll show you:
- How DriftProof locks it down (live)
- Deployment on your stack (takes <5 min)
- Drift verification (PASS/DRIFT binary check)

Meeting link: [Zoom/Teams]  
Time: [Confirmed slot]

— Stephen

---

## Day 3: Post-Demo Follow-Up

**Subject:** DriftProof results on [Company] prompts

---

[FirstName],

Here's what we deployed today:

**Before DriftProof:**
- Your support agent was making refund commitments outside policy
- Output format collapsed into conversational noise
- No way to verify drift without manual review

**After DriftProof (5 min install):**
- Mission locked: "Provide information only. Escalate decisions."
- Constraint cage: "Never promise refunds. Never override policy."
- Format locked: "Issue → Context → Escalation Path"

**Drift verification:**
```
python verify/drift_check.py
→ PASS (all 3 required sections present)
```

**Next step:** Run this on your production prompts for 7 days.

I'll check in Friday to review results.

If it works (it will), we can talk pilot terms.

— Stephen

---

## Day 4: Value Demonstration Email

**Subject:** DriftProof results: Week 1 data

---

[FirstName],

Quick check-in on your DriftProof trial.

**What to look for this week:**
1. Run `drift_check.py` on 10 production outputs
2. Compare to your old outputs (before lockfiles)
3. Count how many would've failed the format check

**Expected result:**  
30-50% of your old outputs violate format/constraints.  
DriftProof outputs: 0% violations (architectural impossibility).

**If you see drift:**  
Something's wrong with the lockfile setup. I'll fix it in 10 min. Just send me the output.

**If you see PASS consistently:**  
You're ready for the pilot contract.

Let's talk terms Friday?

— Stephen

---

## Day 5: Pilot Contract Email

**Subject:** Pilot contract: $25k for 90-day deployment

---

[FirstName],

Based on this week's results, here's the pilot structure:

**Scope:**
- Deploy DriftProof on 3-5 production agents
- Custom lockfiles for each use case
- 90-day monitoring + iteration
- Weekly drift audits + reports
- Full source code + documentation transfer

**Deliverables:**
- Locked prompts (ready for production)
- Drift verification framework (automated)
- Compliance playbook (PDF + training session)
- Case study data (for internal stakeholder buy-in)

**Investment:** $25,000 (one-time)

**Timeline:**
- Week 1: Lockfile deployment + training
- Weeks 2-12: Monitoring + iteration
- Week 13: Final report + handoff

**ROI calc:**  
One avoided compliance violation = $1M+ fine.  
DriftProof prevents that structurally.

Invoice + Stripe link attached.  
Sign → Deploy Monday.

Questions?

— Stephen

P.S. First 3 pilots get priority support + early access to Enterprise tier ($2,999/mo → $1,999/mo for pilot customers).

---

## Payment Link

[Stripe Invoice Link]

**Terms:**
- 50% upfront ($12,500)
- 50% at Week 6 checkpoint ($12,500)
- Net 15 payment terms

---

## Objection Handling Scripts

**Objection:** "We already have prompt monitoring."  
**Response:** "Monitoring detects drift after it happens. DriftProof prevents it architecturally. You're comparing a smoke alarm to fireproof walls."

**Objection:** "Can't we just write better prompts?"  
**Response:** "Prompts decay over time. Context absorption is inevitable in adaptive systems. DriftProof removes the adaptation pathway. The system structurally cannot reinterpret."

**Objection:** "This sounds like over-engineering."  
**Response:** "For creative apps, yes. For compliance-critical systems? This is the minimum viable architecture. One hallucinated diagnosis = lawsuit. DriftProof makes that impossible."

**Objection:** "We need to see ROI data first."  
**Response:** "Fair. Run the 7-day trial. Measure drift violations before/after. If you don't see 30%+ reduction in format/constraint failures, we don't move forward."

**Objection:** "$25k is too much for a proof of concept."  
**Response:** "What's the cost of one compliance failure? One lawsuit? One audit finding? This isn't a POC. It's an insurance policy that deploys in 60 seconds."

---

**Close rate target:** 40% (1 out of 3 demos → pilot)  
**Average time to close:** 5-7 days  
**Bottleneck:** Getting the demo scheduled (most drop at Day 1)

---

**Optimization:**  
Day 1 DM should include a **loom video** (2 min) showing:
1. `./deploy.sh` running
2. `drift_check.py` catching a violation
3. Fixed output passing verification

Subject line: "2-min demo: LLM guardrails that actually work"
