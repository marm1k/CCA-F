# Lab 1

Three standalone exercises against the Claude API (`ANTHROPIC_MODEL`, default `claude-haiku-4-5-20251001`), plus a shared env loader.

- **`env_loader.py`** — loads `ANTHROPIC_API_KEY` (and other vars) from a `.env` file one directory up, without overriding variables already set in the environment.
- **`exercise_1_tool_interfaces.py`** — compares a "weak" toolset (`search`, `lookup` with vague descriptions) against a "strong" toolset (`search_products`, `get_order_status` with explicit usage guidance) on a fixed set of test questions, scoring how often the model picks the correct tool.
- **`exercise_2_structured_errors.py`** — models a flaky orders service that returns structured error envelopes (`isError`, `isRetryable`, `status`) and implements exponential-backoff retry for an agent loop calling `get_order_status`, with a `--check` self-test mode covering malformed IDs, 404s, and recoverable timeouts.
- **`exercise_3_tool_choice.py`** — runs support-ticket triage under `auto`, `any`, and forced tool-choice modes to measure how often the model calls `classify_ticket` cleanly versus drifting to the wrong tool or plain text.

Requires `ANTHROPIC_API_KEY` set in the environment or a `.env` file at the repo root.
