# Lab 3.2 — Targeted Behavior (NorthPeak Services Monorepo)

Starter project for **Lab 3.2: Path-Specific Rules & Plan Mode Workflows**.
Everything you need is already here — your job in the lab is to make Claude
Code's caution scale with the risk of each module.

## What's in here

    CLAUDE.md                       general rules + how path-specific rules work
    src/auth/CLAUDE.md              SECURITY-CRITICAL rules for auth/
    src/orders/CLAUDE.md            order conventions for orders/
    src/payments/CLAUDE.md          MONEY-CRITICAL rules for payments/
    .claude/agents/explorer.md      read-only explorer subagent (Read, Grep, Glob)
    src/auth/tokens.py              verify_token (strict) + deprecated verify_token_v1
    src/orders/service.py           place_order (still calls verify_token_v1)
    src/payments/charges.py         charge (still calls verify_token_v1)
    src/tests/test_smoke.py         pytest suite (4 tests, all green)

The suite starts at 4 tests and grows as you work: Exercise 1 adds one
(-> 5), the Exercise 2 migration adds none (still 5), and Exercise 3 adds
one (-> 6).

## Setup (do this before the session)

1. Get this bundle onto your Blue Labs VM and enter it.
2. Create a virtual environment and install the test dependency:

       python -m venv .venv && source .venv/bin/activate
       # Windows: .venv\Scripts\activate
       pip install -r requirements.txt

3. Confirm the suite is green:

       pytest -q          # expect: 4 passed

4. Start Claude Code **from this folder** so it finds the root CLAUDE.md and the
   per-module ones under src/:

       claude

   The first time, Claude Code will ask you to sign in — follow the prompt.

This project is already a git repository with a committed baseline, so you can
review your changes with `git diff` or undo an experiment with `git restore`.
