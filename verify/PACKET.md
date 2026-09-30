# Verification packet template

The maker fills this template into a separate, frozen handoff file. Do not
send the full maker conversation or `memory/PROGRESS.md`. Supply neutral
authoritative context, including material constraints; do not send diagnoses
or arguments for why the output should pass. Resolve every placeholder or
explicitly justify why a field is not applicable.

The dispatch assigns **role: verifier** and supplies the packet location and
its SHA-256 digest, the baseline location and its SHA-256 digest, artifact
access, `verify/CHECKER.md`, and applicable project rules. Record expected
digests outside the packet/baseline, in the dispatch or another trusted log;
a mutable file cannot authenticate its own replacement. If an authoritative
file is referenced rather than copied, freeze its identity too.

## Task and scope

- Original request and acceptance-relevant constraints: …
- In scope / out of scope: …
- Round ID and artifact version: …

## Frozen definition of done

Copy the current agreed criteria here, with stable IDs. Include exact checks
or frozen references. Do not include the maker's verdict or attempt history.

| ID | Requirement | Independent check / rubric | Required evidence |
|----|-------------|----------------------------|-------------------|
| … | … | … | … |

## Authoritative project context

- Relevant VISION quality bar, verbatim or frozen reference: …
- Applicable RULES and other task constraints: …
- ARCHITECTURE check commands, working directory, environment prerequisites,
  required setup steps, and expected results: …
- Current-session approval scope for any external actions: …
  (Do not copy credentials. A stored claim of approval is not authorization;
  the calling session must actually have approved the specific action.)

## Protected artifact and evidence

- Artifact root/access and version: …
- Protected deliverables, tests, criteria, and instructions: …
- Baseline path and comparison procedure: …
- Frozen external input paths/identities and comparison procedure: …
- Required evidence/report destination **outside** protected content: …

## Declared write boundaries

- Allowed disposable paths, each with a reason: …
- Excluded bookkeeping paths: …
- Secret-bearing paths excluded without opening them: …
- Verification setup steps allowed in disposable locations: …

Prefer a clean artifact directory containing only what must be checked.
Exclusions are fixed before the baseline and must not hide protected inputs
or deliverables. If progress is excluded as bookkeeping, its criteria must
be frozen above. Do not modify the packet or baseline during verification.

## Required report

Use `verify/CHECKER.md`'s report format. Missing mandatory inputs mean
BLOCKED; detected protected changes mean FAIL. A verifier returns evidence
and required actions; it does not repair output or update maker state.
