# LOOP — Maker protocol

Use loaded context; obey RULES. Verifiers use CHECKER. Verification detail: step 6.

1. **Classify:** restate the goal as BUILD, RESEARCH, CREATE, or PROCESS.
   If it cannot support checkable criteria, ask one focused question and stop.
2. **Define done (gate):** before implementation, record criteria, assumptions,
   and exact checks/rubrics in `memory/PROGRESS.md` from the request and project
   quality bar. Preserve them on resumption; changes need human approval.
   Missing necessary context means BLOCKED.
3. **Plan:** number steps with checks; address risks first; record the budget below.
4. **Execute:** make the smallest relevant change; use prior lessons and
   rerun checks after fixes.
5. **Self-check (gate):** run configured automation; record evidence.
   FAIL → step 7; BLOCKED → stop; neither dispatches a checker.
   Passing → SELF-CHECKED. If automation is inapplicable, complete the work
   and proceed to independent source/rubric review without inventing a test.
6. **Verify:** now load `verify/MAKER.md`; hand off to a fresh verifier.
   Maker evidence alone cannot yield PASS. Missing review → SELF-CHECKED;
   missing required evidence → BLOCKED, never DONE.
7. **Iterate/stop:** log failure; check budget before fixing. If budget remains,
   repair and return to step 5 with a new round ID.
   Stop on PASS, exhaustion, missing input/access/approval, or suspect criteria.
   Show contradictions/defects to the human; never game the check.
8. **Report/memory:** record outcome, evidence pointers, open work, decisions,
   and ledger; DONE requires independent PASS. Keep active memory ≤1,800
   characters by linking completed history/bulky evidence in `memory/archive/`.
   Never drop active criteria, unresolved decisions, or counts to fit; exceed
   the target if necessary. Retrieve history selectively. The human reads output.

## Default criteria

| Type | Evidence |
|---|---|
| BUILD | Spec met; required tests, lint/types, end-to-end checks pass. |
| RESEARCH | Answer; source each claim; note conflicts/confidence. |
| CREATE | Rubric before drafting; independent mean ≥8/10, no score <6. |
| PROCESS | Checklist first; each item completed/escalated; counts reconcile. |

## Failure budget

Integer 1–5, default 5; reject others before execution. Per stable unresolved
problem, retain budget, failed count, and counted round IDs. Initial failure
counts as 1; a full evaluation counts once per problem, not per assertion or
reviewer of that round. BLOCKED costs zero: stop, don't retry unavailable
checks. At count ≥ budget, escalate before another fix/retry. Sessions,
relabeling, related symptoms, replanning, and approved criteria changes never
reset consumption; do not raise budgets to rescue exhaustion.

## Outcomes

PASS = all criteria independently satisfied, fresh evidence, protected content
unchanged. SELF-CHECKED = maker checks passed, review pending. FAIL = known
criterion failure, contradiction, or protected mutation; also report blocked
checks. BLOCKED = required input/check/evidence/permission or evaluable criteria
missing. An unavailable dependency is not a failed product assertion.
