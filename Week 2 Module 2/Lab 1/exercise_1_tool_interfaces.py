
import os

import env_loader  

from anthropic import Anthropic

client = Anthropic()
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")


WEAK_TOOLS = [
    {
        "name": "search",
        "description": "Search for stuff in the system.",
        "input_schema": {
            "type": "object",
            "properties": {"q": {"type": "string"}},
            "required": ["q"],
        },
    },
    {
        "name": "lookup",
        "description": "Look up information in the system.",
        "input_schema": {
            "type": "object",
            "properties": {"q": {"type": "string"}},
            "required": ["q"],
        },
    },
]


STRONG_TOOLS = [
    {
        "name": "search_products",
        "description": (
            "Search the NorthPeak product CATALOG for items we sell (tents, "
            "sleeping bags, stoves, boots, etc.) by free-text query. Use this for "
            "availability, price, or whether a product exists. Do NOT use this to "
            "check something a customer already bought — for an existing purchase "
            "use get_order_status instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Free-text product query, e.g. '4 person tent'.",
                },
                "max_results": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_order_status",
        "description": (
            "Retrieve the status of an EXISTING customer order by its order ID "
            "(shipping status, items, tracking). Use this whenever the customer "
            "gives an order number or references a purchase. Do NOT use this to "
            "browse the catalog — for products use search_products instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Order ID in the format 'NP-XXXXXX'.",
                    "pattern": "^NP-[0-9]{6}$",
                },
            },
            "required": ["order_id"],
        },
    },
]

TEST_CASES = [
    {"question": "Do you carry a four-person tent?", "role": "catalog"},
    {"question": "Can you tell me the tracking number for the tent I ordered last week?", "role": "order"},
    {"question": "What's the status of my recent purchase, order number NP-100311?", "role": "order"},
    {"question": "Are waterproof hiking boots currently in stock?", "role": "catalog"},
    {"question": "I ordered the waterproof hiking boots — when will they ship?", "role": "order"},
    {"question": "Do you sell sleeping bags rated for sub-zero winter camping?", "role": "catalog"},
]

ROLE_TO_TOOL = {
    "weak": {"catalog": "search", "order": "lookup"},
    "strong": {"catalog": "search_products", "order": "get_order_status"},
}


def run_harness(label, tools):
    role_to_tool = ROLE_TO_TOOL[label]
    hits = 0
    print(f"\n=== {label.upper()} toolset ===")
    for case in TEST_CASES:
        expected_tool = role_to_tool[case["role"]]
        response = client.messages.create(
            model=MODEL,
            max_tokens=256,
            tools=tools,
            tool_choice={"type": "any"},
            messages=[{"role": "user", "content": case["question"]}],
        )
        tool_calls = [b for b in response.content if b.type == "tool_use"]
        picked = tool_calls[0].name if tool_calls else None
        ok = picked == expected_tool
        hits += ok
        status = "OK  " if ok else "MISS"
        print(f"  [{status}] \"{case['question']}\" -> picked={picked!r} expected={expected_tool!r}")
    print(f"  Total: {hits}/{len(TEST_CASES)}")
    return hits


if __name__ == "__main__":
    weak_hits = run_harness("weak", WEAK_TOOLS)
    strong_hits = run_harness("strong", STRONG_TOOLS)
    print(f"\nSummary: weak={weak_hits}/{len(TEST_CASES)}  strong={strong_hits}/{len(TEST_CASES)}")
