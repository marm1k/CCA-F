---
description: Review current changes against the checklist
allowed-tools: Bash(git diff:*), Bash(git status:*), Read, Grep
argument-hint: "[optional path or scope]"
---

Review the uncommitted changes (focus: $ARGUMENTS). Run `git diff` (and
`git status` if useful) to see what changed, then check each changed hunk
against this checklist:

1. **Tests** — is there a test for every new/changed behaviour (see
   `.claude/rules/testing.md`)?
2. **Purity & validation** — are public functions still pure, with inputs
   validated at the boundary (see `.claude/rules/style.md`)?
3. **Types & docs** — does every public function have type hints and a
   one-line docstring?
4. **Boundaries** — for any threshold logic, are both sides of the boundary
   covered?
5. **Naming** — do new public functions and parameters use full, descriptive
   names (no abbreviations like `qty` or `amt`), matching the existing
   module's naming style?

Group findings as **blocker** / **suggestion** / **nit**, then end with a
one-line verdict, e.g. `Needs changes: 3` or `Looks good: 0 blockers`.

Do not edit any files — this command is read-only.
