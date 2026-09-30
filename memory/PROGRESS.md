# Active memory

Goal: slim and push `codex/verification-contract`; no merge.
Status: IN PROGRESS

## Done criteria
- C1: startup ≤8,500 characters (AGENTS, LOOP, VISION, ARCHITECTURE, RULES,
  PROGRESS once each); AGENTS+LOOP+RULES ≤5,000; active memory ≤1,800.
  Characters/4 is an estimate, not measured model tokens.
- C2: archive prior completed memory verbatim; retain active criteria,
  unresolved decisions, and retry consumption.
- C3: identical entry files; preserve roles, approval/criteria gates, outcomes,
  retries, injection/secret rules, and integrity safeguards.
- C4: load verification detail only at that stage; no reviewer for failed or
  blocked maker checks; no-automation tasks still get independent rubric review.
- C5: tests, budget checks, links, whitespace, and independent review pass;
  push this branch and verify remote SHA equals HEAD.

## Plan
1. Compact/archive; measure reading sets.
2. Defer verification detail; check safeguards.
3. Test/review; push; compare remote HEAD.

## Retry ledger
| Problem | Budget | Failed rounds | Counted IDs |
|---|---:|---:|---|
| context-budget | 5 | 4 | baseline, draft-1, draft-2, draft-3 |

## Current evidence / next action
23 tests and independent review PASS; source integrity unchanged.
Core 4,878 characters. Budget issue resolved; push pending.
Token thresholds cover shipped templates, not arbitrary project content.

## Relevant history
[Verified safeguards and publication](archive/2026-09-verification-contract.md).
[Current measurements/evidence](archive/2026-09-context-budget.md).
Retrieve selectively.
