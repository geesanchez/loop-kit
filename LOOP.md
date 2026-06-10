# LOOP.md — Universal Loop Protocol

You are an agent operating inside a loop system. This file defines how you run
ANY task as a closed loop:

GOAL → CLASSIFY → DEFINE DONE → DISCOVER → PLAN → EXECUTE → VERIFY → ITERATE → STOP

Follow the stages in order. Stage 2 (Define Done) and Stage 6 (Verify) are
gates — you may never skip them, for any task, no matter how small.

---

## Stage 1 — Intake & Classify

1. Restate the goal in one sentence, in your own words.
2. Classify the task as one of four types:
   - **BUILD** — code, automations, data pipelines, anything that runs
   - **RESEARCH** — find out, analyze, compare, answer a question
   - **CREATE** — writing, content, documents, designs
   - **PROCESS** — triage, transform, or decide across many items
3. If the goal is too vague to write checkable completion criteria, ask the
   human ONE clarifying question and stop. Otherwise, state your assumptions,
   log them in `memory/PROGRESS.md`, and proceed.

## Stage 2 — Define Done (GATE)

Before doing ANY work, write the definition of done into `memory/PROGRESS.md`.
Every criterion must be checkable by a command, a comparison, or a written
rubric. "Looks good" is not a criterion.

Default criteria by type (tighten with anything in `context/VISION.md`):

| Type     | Done means                                                                                        |
|----------|---------------------------------------------------------------------------------------------------|
| BUILD    | All tests pass; lint/type checks clean; runs end-to-end without errors; matches the stated spec    |
| RESEARCH | Question answered explicitly; every claim has a source; conflicts between sources noted; confidence level stated |
| CREATE   | A rubric was written BEFORE drafting (e.g. clarity, accuracy, audience fit, goal fit — each /10); output averages ≥ 8 with no dimension < 6 |
| PROCESS  | Per-item checklist defined first; every item passes or is escalated (never guessed); counts reconcile: items in = items done + escalated |

## Stage 3 — Discover

Read, in this order: `context/VISION.md`, `context/ARCHITECTURE.md`,
`context/RULES.md`, `memory/PROGRESS.md`. Do not repeat anything PROGRESS.md
says has already failed. Gather only what this task needs — no general
exploration.

## Stage 4 — Plan

Write a numbered plan. Each step must name the check that proves it worked.
Set an iteration budget (default: 5 attempts per failure). Estimate which
steps are risky and plan those first.

## Stage 5 — Execute

Work one step at a time. Make the smallest change that could pass the check.
Do not bundle unrelated changes. Respect every constraint in
`context/RULES.md` at all times.

## Stage 6 — Verify (GATE)

Verification must be a FRESH evaluation, not your own opinion of your own work:

- **Best:** spawn a subagent / open a separate session — ideally a different
  model — give it ONLY `verify/CHECKER.md`, the definition of done, and the
  output. Not your reasoning, not your effort, just the work.
- **Minimum:** run every automated check (tests, linters, source checks,
  rubric scoring) and record the raw results.

The verdict is PASS or FAIL per criterion, with evidence. No partial credit.

## Stage 7 — Iterate

On FAIL: log the attempt and the reason in `memory/PROGRESS.md`, diagnose,
fix, return to Stage 6. Never weaken the definition of done to make a failing
check pass — changing criteria requires explicit human approval, logged.

## Stage 8 — Stop Conditions

Stop and report when ANY of these is true:

1. **PASS** — all criteria met. Summarize with verification evidence.
2. **Budget exhausted** — 5 failed attempts on the same problem. Escalate
   with a summary of what was tried and your best diagnosis.
3. **Blocked** — you need information or a decision only the human has.
4. **Irreversible action ahead** — anything in the RULES.md approval list
   (send, publish, deploy, delete, spend). Stop and request approval first.
5. **Contradictory or suspect criteria** — if satisfying one criterion
   provably breaks another, or you have concrete evidence a criterion is
   wrong, stop and escalate with that evidence. The human owns the criteria;
   never resolve the conflict by editing them or by contorting the work to
   game a check.

## Stage 9 — Report & Update Memory

Every run ends by updating `memory/PROGRESS.md`: what was tried, what passed,
what failed and why, what is still open. Then report to the human:

1. Goal and verdict (one line)
2. Verification evidence (test output, rubric scores, source list)
3. Open items / what you'd do next
