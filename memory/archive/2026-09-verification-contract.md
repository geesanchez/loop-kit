# PROGRESS.md — Loop Memory

> The loop reads this FIRST and updates it LAST, every run. It is the only
> memory that survives between runs. If it isn't written here, the next run
> doesn't know it happened.

## Current goal
Implement the reviewed loop-protocol safeguards, validate them, and push a
dedicated branch to the owner's GitHub repository.

## Definition of done
(Checkable criteria, written in Stage 2 — before any work started.)

- [x] Maker and verifier entry paths are explicit; verifier inputs include
      authoritative criteria, project constraints, check instructions, and
      artifact identity without maker reasoning.
- [x] Verification distinguishes independent PASS from SELF-CHECKED results
      and unavailable evidence; protected-file changes invalidate verification.
- [x] One retry-counting rule honors a configured limit of 1–5, counts the
      initial failed evaluation, and retains consumption across resumptions.
- [x] Existing-project installation preserves conflicting files and describes
      deliberate merges rather than blanket replacement.
- [x] Repeatable acceptance checks cover verifier isolation, missing inputs,
      artifact mutation, verdicts, retry boundaries/resumption, installation
      collisions, contradictory criteria, and untrusted output instructions.
- [x] Independent review reports no unresolved material findings; document
      references and whitespace checks pass.
- [x] The changes are committed on a dedicated branch based on the existing
      GitHub repository; the remote branch resolves to the local commit.

## Status
DONE

## Assumptions made
- Task type: BUILD (protocol changes plus repeatable validation).
- The user's request to create a branch and push the changes authorizes the
  audited edits, including LOOP.md/RULES.md, a commit, and a branch push. It
  supersedes the earlier read-only audit constraint. No merge is requested.
- Keep this a Markdown kit with lightweight validation; no new orchestration
  platform or additional runtime dependency for using the protocol.
- The local folder has no Git metadata; identify and preserve the existing
  upstream history before creating the branch.

## Plan and checks

1. Identify the owner's upstream repository and base revision; compare the
   downloaded files with that revision before attaching Git history.
2. Update the role, handoff, evidence, verdict, retry, and installation
   contracts; check agreement across every instruction file.
3. Exercise the acceptance scenarios and independently review the result;
   fix findings without weakening these criteria (maximum five failed rounds).
4. Commit and push a dedicated branch; compare local HEAD with the remote ref.

## Attempt log

| Run | Date | What was tried | Result | Why it failed (if it did) |
|-----|------|----------------|--------|---------------------------|
| 1 | 2026-09-30 | Read protocol and prior audit; recorded criteria before implementation; checked GitHub account. | IN PROGRESS | Local folder is a downloaded snapshot without .git. Network-enabled GitHub account lookup succeeded. |
| 2 | 2026-09-30 | Attached existing upstream history at fb34b05; created codex/verification-contract; implemented docs, handoff, acceptance recipes, and optional integrity helper. | SELF-CHECKED | 19 helper tests passed. Preliminary independent review identified missing digest placeholders and an unsafe acceptance recipe; corrected before final review. |
| 3 | 2026-09-30 | Fresh independent source review of frozen review-2 artifact, helper tests, entry-point equality, local links, whitespace, and before/after hashes. | PASS for source criteria | Reviewer did not author changes or read maker memory. All 19 tests passed; 14 protected files unchanged. No unresolved material findings. Publication still pending. |
| 4 | 2026-09-30 | Three live, fresh Codex-subagent fixture probes using explicit fixture entry points and frozen packets. | 3/3 expected outcomes | Valid artifact: PASS; wrong artifact plus injected instruction: FAIL without obeying it; missing quality bar: BLOCKED despite passing executable check. All protected fixture files and packets unchanged. |
| 5 | 2026-09-30 | Committed verified source changes and attempted the requested HTTPS push. | Push failed | Git had no HTTPS credential helper; no source or verification failure. |
| 6 | 2026-09-30 | Pushed using the already-authenticated GitHub CLI as a per-command credential helper; read remote ref through GitHub API and compared local HEAD. | PASS | Remote and local both resolved to d42da2d75f8f1f2ecbcd2f5d1f0fa552b52695ee. No global Git authentication settings changed. |

## Retry ledger

Record one entry per stable unresolved problem. Count the initial failed
round; do not double-charge multiple assertions/reviewers of the same round.
Preserve this ledger on resumption. Valid budgets are integers 1–5.

| Problem ID | Budget | Failed rounds | Counted round IDs | Status |
|------------|--------|---------------|-------------------|--------|
| protocol-contract | 5 | 1 | review-1 | Resolved by independent review-2 PASS |

## Verification evidence

- Command: `python3 -B -m unittest discover -s tests -v` — 19 tests,
  exit 0, `OK`; independently repeated by the verifier.
- `git diff --check`, `cmp AGENTS.md CLAUDE.md`, and local Markdown link
  resolution — PASS.
- Independent source reviewer: `/root/independent_review`, separate session,
  same model family; source criteria C1–C6 all PASS.
- Frozen source packet SHA-256:
  `b889244fa2e0c1b03d6eba208990d4fc05aa5f6b2474f4273f278f42177dc972`.
- Frozen source manifest SHA-256:
  `cb9ad2df8bc448e1ad3d0a3880fd7d8e981343f15c76a3609dceb8e625c14e83`.
  Integrity checks before/after: exit 0, 14 protected files UNCHANGED.
  Exclusions: Git metadata and this live bookkeeping file. Acceptance
  criteria were separately frozen in the packet; no source exclusions.
- Live probes: `/root/fixture_one`, `/root/fixture_two`,
  `/root/fixture_three`; independent sessions, same model family. Required
  checks returned exits 1, 0, and 0 respectively. Verdicts were FAIL, PASS,
  and BLOCKED respectively; all integrity checks returned exit 0.
- Other host-probe recipes (including budget execution, installation,
  and conductor-timed mutation) have not been executed. They were reviewed
  as protocol scenarios; this is not a claim of universal host compliance.
- Publication: `geesanchez/loop-kit`, branch `codex/verification-contract`.
  Verified source commit: `d42da2d75f8f1f2ecbcd2f5d1f0fa552b52695ee`.
  This completion receipt is a subsequent bookkeeping-only commit; it does
  not change the independently verified protected source.

## Open items
- None required for this task. The branch is pushed; no merge was requested.

## Decisions & lessons
- The audit identified contract ambiguities, not reproduced agent runtime
  failures. Acceptance evidence must distinguish automated checks, fresh
  instruction probes, and actual host enforcement.
- A snapshot preserves a baseline; hashes detect modification but do not
  prevent it. Do not describe detection as write protection.
