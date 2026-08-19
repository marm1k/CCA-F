

import os

import env_loader  

from anthropic import Anthropic

client = Anthropic()
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")

CLASSIFY_TOOL = {
    "name": "classify_ticket",
    "description": "Classify a support ticket into exactly one routing category.",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["order_issue", "product_question", "return_request", "other"],
            },
            "reason": {"type": "string"},
        },
        "required": ["category", "reason"],
    },
}


DRAFT_REPLY_TOOL = {
    "name": "draft_customer_reply",
    "description": "Draft a plain-text reply to send directly to the customer.",
    "input_schema": {
        "type": "object",
        "properties": {
            "reply_text": {"type": "string", "description": "The drafted reply."},
        },
        "required": ["reply_text"],
    },
}

TOOLS = [CLASSIFY_TOOL, DRAFT_REPLY_TOOL]

TICKETS = [
    "My order NP-100245 hasn't arrived and it's been two weeks. Where is it?",
    "Do you have any tents rated for below-freezing temperatures?",
    "I want to return the hiking boots I bought — they don't fit. How do I start a return?",
    "Hey, just wanted to say your site's new redesign looks awesome!",
]

modes = {
    "auto": {"type": "auto"},
    "any": {"type": "any"},
    "FORCED": {"type": "tool", "name": "classify_ticket"},
}


def run_ticket(ticket_text, tool_choice):
    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        tools=TOOLS,
        tool_choice=tool_choice,
        messages=[{"role": "user", "content": ticket_text}],
    )
    tool_calls = [b for b in response.content if b.type == "tool_use"]
    text_blocks = [b.text for b in response.content if b.type == "text"]

    if any(c.name == "classify_ticket" for c in tool_calls):
        call = next(c for c in tool_calls if c.name == "classify_ticket")
        return f"classify_ticket(category={call.input.get('category')!r})"
    if any(c.name == "draft_customer_reply" for c in tool_calls):
        return "draft_customer_reply(...)  <- WRONG TOOL for triage"
    if text_blocks:
        return f"plain text: {' '.join(text_blocks)[:60]!r}"
    return f"stop_reason={response.stop_reason}, no tool call and no text"


if __name__ == "__main__":
    clean_counts = {}
    for mode_name, tool_choice in modes.items():
        print(f"\n=== mode: {mode_name} ({tool_choice}) ===")
        clean = 0
        for ticket in TICKETS:
            outcome = run_ticket(ticket, tool_choice)
            is_clean = outcome.startswith("classify_ticket(")
            clean += is_clean
            print(f"  [{'clean' if is_clean else 'DRIFT'}] \"{ticket[:45]}...\" -> {outcome}")
        clean_counts[mode_name] = clean
        print(f"  Clean classifications: {clean}/{len(TICKETS)}")

    print("\nSummary:")
    for mode_name, count in clean_counts.items():
        print(f"  {mode_name:8s}: {count}/{len(TICKETS)} tickets got a clean classify_ticket call")
