---
name: changelog-entry
description: >
  Use when the user wants to add a CHANGELOG entry, write release notes,
  update the changelog, or summarize a change for a change log.
---

# Changelog Entry

1. Run `git diff` to see what actually changed. If there is nothing in the
   diff, say so and stop — there is nothing to log.
2. Skip purely formatting-only edits (whitespace, comment wording) unless
   they are the only change.
3. Group each remaining change under one of: `Added`, `Changed`, `Fixed`,
   `Removed`.
4. Write each entry as a short, user-facing sentence — describe the effect
   for someone using the library, not the implementation detail (e.g.
   "Optional gift-wrap fee helper for orders." not "Added
   `gift_wrap_fee` function").
5. Prepend the entry under a `## [Unreleased]` heading at the top of
   `CHANGELOG.md`, creating the file if it does not exist yet. If an
   `## [Unreleased]` section already exists, add to it instead of creating a
   duplicate heading.

Output format:

```
## [Unreleased]

### Added
- <user-facing sentence>
```
