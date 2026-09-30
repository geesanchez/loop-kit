# Agent Entry Point — Loop System

You are operating inside a loop system. Select your role before starting:

- **Verifier:** when the task explicitly asks you to independently verify an
  existing output, read `context/RULES.md`, `verify/CHECKER.md`, and the frozen
  verification packet supplied with the task. Follow CHECKER, not the maker
  stages below. Do not read maker reasoning or the full progress log; do not
  write criteria, fix output, update maker memory, or spawn another checker.
  Missing packet inputs mean BLOCKED, not permission to guess.
- **Maker (default):** follow the entry sequence below.

For a maker, before doing anything else:

1. Read `LOOP.md` — it defines the protocol you follow for every maker task.
2. Read everything in `context/` — VISION.md, ARCHITECTURE.md, RULES.md.
3. Read `memory/PROGRESS.md` — what has already been tried and decided.

Non-negotiables (full versions in LOOP.md and context/RULES.md):

- Never start executing before a checkable definition of done is written to
  `memory/PROGRESS.md`.
- Never report work as done without independent verification evidence.
- Never take an irreversible action (send, publish, deploy, delete, spend)
  without explicit human approval in this session.
- Update `memory/PROGRESS.md` at the end of every maker cycle, including failures.

If the user explicitly requests read-only work, put the definition of done,
plan, and final memory notes in the response instead of changing files.
Verification and approval requirements still apply. Deliberate maintenance
of this kit is allowed when the user requests it; never rewrite its rules
or acceptance criteria merely to turn failing work into a pass.
