---
description: Run the pytest suite and summarize pass/fail
allowed-tools: Bash(python -m pytest:*), Bash(py -3 -m pytest:*), Read
argument-hint: "[optional test path or -k expression]"
---

Run the project's test suite: `python -m pytest -q $ARGUMENTS` (fall back to
`py -3 -m pytest -q $ARGUMENTS` on Windows if `python` is not on PATH).

Report:

- The pass/fail count from the run.
- If everything passed, a one-line confirmation.
- If something failed, name the failing test(s), quote the relevant
  assertion/traceback line, and give a one-sentence likely cause — do **not**
  edit any code.
