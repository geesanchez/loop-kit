# Context-budget evidence

Task: reduce recurring text on codex/verification-contract; retain safeguards,
push the branch, and do not merge. Active criteria/ledger remain in PROGRESS.

## Preserved acceptance thresholds

- Startup: AGENTS + LOOP + VISION + ARCHITECTURE + RULES + PROGRESS, once
  each, at most 8,500 characters with the shipped context templates.
- Instructions: AGENTS + LOOP + RULES, at most 5,000 characters.
- Active memory: at most 1,800 characters in this kit. Never discard needed
  state to enforce this target in another project.
- Preserve roles, approval/criteria gates, outcomes, retry semantics,
  injection/secret rules, integrity, and independent final verification.
- Archive previous completed memory verbatim. Defer detailed verification
  loading; known failing/blocked self-checks do not dispatch a reviewer.
  Tasks without configured automation still receive independent rubric review.
- Tests, links, whitespace, independent review and remote equality required.

## Budget attempts (same problem: context-budget, limit 5)

1. Baseline: new budget tests failed on the uncompacted documents, including
   the newly appended task criteria. Instruction total 13,095 characters;
   startup 23,117; memory 8,544. Entry equality passed.
2. draft-1: comparison failed, instructions 6,222; startup 9,329.
3. draft-2: 22/23 tests passed; instructions 5,110 exceeded 5,000.
4. draft-3: 22/23 tests passed; instructions 5,029 exceeded 5,000.
5. draft-4: all 23 tests passed; instructions 4,878. The issue is resolved
   after four consumed failed rounds; no criterion or threshold was weakened.

## Executed evidence

- `python3 -B -m unittest discover -s tests -v`: 23 tests, exit 0, OK
  (19 integrity tests plus four context/entry regression tests).
- `git diff --check`: exit 0.
- Local Markdown links resolved; AGENTS and CLAUDE are byte-identical.
- Previous archive matches `git show 93b9896:memory/PROGRESS.md` byte-for-byte.
- Before slimming, committed startup text was 21,702 characters; the original
  main kit was 8,881. Draft-4 was 8,109 before updating active bookkeeping;
  final published figures must be measured again after that update.
- Character/4 figures are rough estimates, not tokenizer or billing data.

## Independent review

Fresh same-model reviewer `/root/compact_independent_review`: PASS on C1–C5,
no material findings. Independently ran all 23 tests, checked references,
archive byte equality, entry equality, and safety/dispatch source traces.
No new live host-compliance probes were performed in this compression cycle.

- Frozen packet SHA-256:
  `1106fdd648cc145dcaa461e65423d4c0cd334be54ec31a0f4295721dd66f1f0b`.
- Baseline SHA-256:
  `f900d30c4ef6987852a24a28bd8ece5fd037db9bc98a0ec4fb9c727d516654d3`.
- Before/after: exit 0, 17 protected files UNCHANGED. Only Git metadata,
  active memory and this evidence record excluded as bookkeeping; criteria
  were separately frozen. No source exemption.
- Reviewed startup 7,959 characters (estimated 1,989.75 tokens); instructions
  4,878; active memory 1,603. This is 63.3% less startup text than 93b9896.
  Small bookkeeping updates may alter the final count; budget tests are
  rechecked after those changes. Original main was 8,881 characters.

## Publication

Source commit `817a8b17cd4ec7e9c901b7e3167a73e815435b86` was pushed to
`geesanchez/loop-kit`, branch `codex/verification-contract`. GitHub's ref API
and local HEAD returned that same SHA. No merge was performed. This receipt
is a subsequent bookkeeping-only commit; protected source is unchanged.

No host-wide behavioral guarantee or billing measurement is inferred from
text-length checks.
