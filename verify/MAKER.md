# Prepare independent verification

Load this at LOOP's verification step, not at startup. Run configured
automated checks first: known FAIL returns to the repair/budget step;
BLOCKED stops. Do not spend an independent review on either. When automation
is inapplicable, use the agreed independent source checks or rubric.

1. Fill `verify/PACKET.md` into a separate frozen handoff: original task/scope,
   criteria, relevant quality bar/rules, exact check commands and prerequisites,
   artifact identity, and write boundaries. Copy criteria from active memory,
   not its full log. Resolve placeholders; omit maker reasoning, diagnoses,
   attempt history, and persuasion. Required context must not be omitted.
2. Protect deliverables, tests, criteria, and verification instructions. Prefer
   a clean artifact directory. Otherwise declare exclusions for bookkeeping,
   disposable caches/dependencies, and secret-bearing paths before baselining;
   never read secrets to hash them. Exclusions cannot hide acceptance inputs
   or deliverables. Freeze criteria separately if live memory is excluded.
3. Store the content baseline outside the writable artifact. Record its
   SHA-256 and the frozen packet's SHA-256 separately in the trusted dispatch,
   outside both mutable files. Freeze referenced external inputs too.
   `verify/integrity.py` optionally detects added, removed, and changed files.
   Comparison detects differences; it does not prevent writes, sandbox checks,
   or detect transient writes later restored. Use host restrictions as needed.
4. Dispatch a fresh session/subagent with no maker conversation in the
   **verifier** role, preferably a different model family. Provide CHECKER,
   the completed packet, applicable rules, artifact access, expected digests,
   and an external report destination. The checker must independently execute
   required checks and compare protected inputs/output before and after.
   Only predeclared disposable paths may change. Any altered packet, baseline,
   or protected artifact invalidates the result, even when tests pass; the
   checker never replaces a failing baseline.
5. Record its per-criterion evidence and overall outcome using LOOP's labels.
   PASS requires every criterion independently satisfied; missing evidence
   is BLOCKED, and known failure remains FAIL despite other blocked checks.
   No reviewer means nonfinal SELF-CHECKED, not DONE. The verifier never fixes
   output or updates maker state; the maker records failures in its ledger.

On repair or an approved criteria change, invalidate prior evidence, prepare
a new artifact/packet/baseline, and retain retry history. Reporting may update
predeclared bookkeeping after review, but changing protected deliverables or
frozen criteria requires fresh verification. Keep the full evidence in a
linked archive; active memory needs only its result and retrieval pointer.
