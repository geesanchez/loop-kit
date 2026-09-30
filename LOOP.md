# LOOP.md — Universal Loop Protocol

This is the **maker** workflow:

GOAL → CLASSIFY → DEFINE DONE → DISCOVER → PLAN → EXECUTE → VERIFY → ITERATE → STOP

An explicitly assigned **verifier** follows `verify/CHECKER.md` instead. It
does not execute this maker loop, change criteria, repair output, update
maker memory, or commission another verifier. Both roles obey applicable
project rules and the user's instructions.

Define Done and Verify are gates. For an explicitly read-only task, record
the criteria, plan, and memory notes in the response instead of files.

## Stage 1 — Intake & Classify

1. Restate the goal in one sentence.
2. Classify it as **BUILD** (anything that runs), **RESEARCH** (an answer or
   analysis), **CREATE** (content or design), or **PROCESS** (many items).
3. If completion cannot be defined yet, ask one focused question and stop
   before execution. Otherwise record assumptions in `memory/PROGRESS.md`.
4. On resumption, read the existing criteria, decisions, and retry ledger
   before writing. Preserve them; starting a new session is not a new task.

## Stage 2 — Define Done (GATE)

Before implementation, write checkable criteria to `memory/PROGRESS.md`.
Use the user's request and relevant `context/VISION.md` constraints. Retain
existing criteria on resumption. Every criterion needs a command, comparison,
or written rubric; include the exact check procedure or an authoritative
reference. Criteria changes after work begins require human approval and a
record of the change. Do not silently replace criteria on restart.

| Type | Default criteria |
|------|------------------|
| BUILD | Required tests, lint/type checks, and end-to-end checks pass; output matches the stated spec. |
| RESEARCH | Question answered; claims sourced; source conflicts noted; confidence stated. |
| CREATE | Rubric defined before drafting; independent scores average ≥ 8/10 with no dimension < 6. |
| PROCESS | Checklist defined before processing; every item passes or is escalated; input count = completed + escalated. |

## Stage 3 — Discover

Read `context/VISION.md`, `context/ARCHITECTURE.md`, `context/RULES.md`, and
`memory/PROGRESS.md`. Reuse prior evidence and lessons; do not repeat a failed
approach without a reason. Re-running a check after a relevant fix is expected.
Gather only what the task needs. Missing required project context is BLOCKED.

## Stage 4 — Plan

Write a numbered plan, with a named check for each step; address risky steps
first. Set a **failure budget**, an integer from **1 to 5**, default **5**.
Reject values outside that range before execution.

Keep a retry ledger in `memory/PROGRESS.md`: stable problem ID, selected
budget, failed-round count, and the IDs of rounds already counted. A round
is one evaluation of the required checks for an artifact version:

- The **initial failed evaluation counts as 1**. Each later failed round
  adds 1 for each unresolved problem it demonstrates, even if the problem
  produces several failed assertions. Do not count each assertion separately.
- Maker checks and independent review of the same round do not charge the
  same problem twice. Give a repaired artifact a new round ID.
- BLOCKED checks are not failed assertions and do not consume the budget.
  Stop to resolve the blocker; do not repeatedly rerun an unavailable check.
- Preserve counts across sessions, handoffs, and related symptoms of the
  same problem. Renaming an issue, changing criteria, or replanning does not
  reset its count. Do not increase the chosen budget to rescue a failure.
- At `failed rounds >= selected budget`, stop **before** another fix/retry
  for that problem and escalate. Five is a ceiling, not a required minimum.

## Stage 5 — Execute

Make the smallest change needed for the next check. Do not bundle unrelated
changes. Apply `context/RULES.md` throughout execution, including before any
check command with side effects. Existing session approval for the specific
action is sufficient; do not request the same approval again.

## Stage 6 — Verify (GATE)

1. Run the required maker checks and record commands, exit results, and
   evidence. Passing these checks alone yields **SELF-CHECKED**, not final PASS.
2. Prepare a frozen handoff using `verify/PACKET.md`: original task/scope,
   criteria, relevant quality bar and rules, exact check instructions and
   prerequisites, artifact identity, and the approved write boundaries.
   Supply authoritative context, not maker diagnoses, attempts, or persuasion.
   Copy criteria from progress into the packet; do not hand over the full log.
3. Identify the protected deliverables, tests, criteria, and verification
   instructions. Use a clean artifact directory or explicitly exclude known
   bookkeeping, disposable caches, dependencies, and secret-bearing paths
   **before** taking a baseline. Never inspect secrets to compute their hashes.
   Exclusions must not hide deliverables or acceptance inputs. Freeze criteria
   separately if the live progress log is excluded as bookkeeping.
4. Record a content manifest and its digest outside the writable artifact;
   send the expected digest separately in the verifier dispatch. Freeze the
   packet too, recording its digest outside the packet. The optional
   `verify/integrity.py` helper detects added, removed, and changed files.
   A snapshot or hash detects changes when compared; it does not prevent
   writes or sandbox executable code. Use actual host restrictions if needed.
5. Dispatch a fresh session/subagent in the verifier role, preferably a
   different model family, with CHECKER, the packet, applicable rules, artifact
   access, and the expected digests. Do not inherit the maker conversation.
   The verifier runs the specified checks and compares the protected artifact
   and frozen inputs before and after checking. Only declared disposable paths
   may change. An altered baseline, packet, or protected artifact is FAIL,
   even if tests pass. The verifier never refreshes a failing baseline.

Use these outcomes consistently:

| Outcome | Meaning and next action |
|---------|-------------------------|
| PASS | Independent verifier evaluated every criterion with fresh evidence; required inputs and protected artifacts remained unchanged. Report completion. |
| SELF-CHECKED | Maker checks passed, but independent evaluation is pending/unavailable. Report non-final status; do not mark DONE. |
| FAIL | A checkable criterion failed, criteria contradict each other, or protected content changed. Record evidence and apply the retry/escalation rules. |
| BLOCKED | A required input, prerequisite, permission, or check result is unavailable, or criteria cannot be evaluated. State what is missing; never infer PASS. |

A known failure remains FAIL if other checks are BLOCKED; report both per
criterion. An unavailable dependency alone is BLOCKED, not proof the output
is defective. No required criterion may be skipped to obtain PASS.

## Stage 7 — Iterate

On FAIL, record the round and evidence, update the retry ledger once, and
check the stop conditions **before** repairing. If budget remains and the
criteria are valid, fix the output, prepare a new artifact baseline/packet,
and return to Stage 6. Never weaken criteria, adjust tests to hide defects,
or change the protocol to make failing work pass. An approved criteria change
invalidates prior verification and does not erase the retry history.

## Stage 8 — Stop Conditions

Stop and report when any condition applies:

1. **PASS:** all criteria independently verified with evidence.
2. **Budget exhausted:** the chosen failure budget for an unresolved problem
   has been reached. Include its ledger and best diagnosis.
3. **BLOCKED / SELF-CHECKED:** required information, access, a decision, or
   independent review is missing. Identify the next action; do not claim done.
4. **Unapproved irreversible action:** obtain explicit session approval for
   sending, publishing, deploying, deleting irreversibly, or spending before
   the action. A specific approval already given in this session still applies.
5. **Contradictory or suspect criteria:** show the evidence and escalate to
   the human. Vague criteria need clarification; incorrect criteria need an
   approved correction. Do not contort output to satisfy a broken check.

## Stage 9 — Report & Update Memory

The maker records results, raw evidence locations, outcome, retry ledger,
decisions, and open items in `memory/PROGRESS.md`, including failed/blocked
runs. Reporting may update declared bookkeeping after review; it must not
alter the frozen criteria or protected deliverables. A subsequent change to
either requires fresh verification of the new version.

Report the goal and outcome, verification evidence (including reviewer and
artifact identity), and remaining actions. Mark DONE only after PASS. The
human still reads the output before relying on or approving its use.
