# Lab 1.1 — Building the Agentic Loop

`Lab_1_1_Agentic_Loop.ipynb` walks through a support-ticket triage pipeline with the Claude API, in four stages:

1. **The agentic loop (S1)** — a `while True` loop around `client.messages.create` that dispatches `tool_use` calls, appends `tool_result`s, and exits on `stop_reason == "end_turn"`.
2. **Coordinator & subagents (S2)** — a classifier, CRM enricher, drafter, and validator, each a separate Claude call chained together by a coordinator function.
3. **Explicit context passing (S3)** — a `TicketContext` dataclass that carries required fields between subagents instead of relying on shared conversation history, failing fast (`TypeError`) on missing fields.
4. **Programmatic step enforcement (S4)** — `gate_*` functions that raise a `PipelineGateError` and halt the pipeline if a prior stage's output is incomplete, demonstrated both passing and deliberately sabotaged.

Each stage ends with reflection questions on `stop_reason` handling, subagent memory isolation, and why gates (code) are more reliable than prompt instructions alone.

Requires `ANTHROPIC_API_KEY` set in the environment or a `.env` file at the repo root.
