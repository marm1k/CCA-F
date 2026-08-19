# CCA-F

Coursework and lab exercises built around the Anthropic (Claude) API, organized by week/module.

## Contents

- [Week 1 Module 1](Week%201%20Module%201/) — the agentic tool-use loop, subagent coordination, and pipeline gates.
- [Week 2 Module 2](Week%202%20Module%202/) — tool interface design, structured error handling, and tool-choice control.

## Setup

Each lab reads `ANTHROPIC_API_KEY` from environment variables (loaded from a local `.env` file, which is intentionally untracked — see `.gitignore`). Create your own `.env` at the repo root:

```
ANTHROPIC_API_KEY=your-key-here
```
