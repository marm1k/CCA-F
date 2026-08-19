import json
import os
import re
import sys
import time

import env_loader 

from anthropic import Anthropic

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")

ORDER_ID_PATTERN = re.compile(r"^NP-[0-9]{6}$")
RETRYABLE = {408, 429, 500, 502, 503, 504}

class ServiceError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message



_call_counts = {}


ALWAYS_404 = {"NP-999999"}
FLAKY_ONCE_THEN_OK = {"NP-100245"}  


def orders_service(order_id):
    """Raises ServiceError for bad/missing orders; otherwise returns order data."""
    if not ORDER_ID_PATTERN.match(order_id):
        raise ServiceError(400, f"Malformed order id: {order_id!r}. Expected format NP-XXXXXX.")

    _call_counts[order_id] = _call_counts.get(order_id, 0) + 1
    attempt = _call_counts[order_id]

    if order_id in ALWAYS_404:
        raise ServiceError(404, f"No such order: {order_id}")

    if order_id in FLAKY_ONCE_THEN_OK and attempt == 1:
        raise ServiceError(504, "Gateway timeout contacting Orders service")

    return {
        "order_id": order_id,
        "status": "shipped",
        "carrier": "UPS",
        "tracking": "1Z999AA10123456784",
        "items": ["4-Person Tent"],
    }



def call_order_tool(order_id):
    try:
        data = orders_service(order_id)
        return {"isError": False, **data}
    except ServiceError as err:
        return {
            "isError": True,
            "isRetryable": err.status in RETRYABLE,
            "status": err.status,
            "error": err.message,
        }


def run_with_retry(order_id, max_attempts=4):
    delay = 0.2
    for attempt in range(1, max_attempts + 1):
        result = call_order_tool(order_id)
        if not result["isError"]:
            return result
        if result["isRetryable"] and attempt < max_attempts:
            time.sleep(delay)
            delay *= 2  
            continue
        return result  
    return result



GET_ORDER_STATUS_TOOL = {
    "name": "get_order_status",
    "description": (
        "Retrieve the status of an EXISTING customer order by its order ID "
        "(shipping status, items, tracking). Use this whenever the customer "
        "gives an order number or references a purchase."
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
}


def run_agent_turn(client, user_message, max_iterations=6):
    messages = [{"role": "user", "content": user_message}]
    for iteration in range(1, max_iterations + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=512,
            tools=[GET_ORDER_STATUS_TOOL],
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            final_text = "".join(b.text for b in response.content if b.type == "text")
            print(f"  final ({response.stop_reason}): {final_text}")
            return

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            order_id = block.input.get("order_id", "")
            envelope = run_with_retry(order_id)
            print(f"  [iter {iteration}] get_order_status({order_id!r}) -> {envelope}")
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(envelope),
                    "is_error": envelope["isError"],
                }
            )
        messages.append({"role": "user", "content": tool_results})

    print("  stopped: exceeded max_iterations")


def self_check():
    failures = 0

    def check(label, condition):
        nonlocal failures
        print(f"  [{'PASS' if condition else 'FAIL'}] {label}")
        if not condition:
            failures += 1

    _call_counts.clear()
    good = call_order_tool("NP-100311")
    check("good id succeeds", good["isError"] is False and good["order_id"] == "NP-100311")

    _call_counts.clear()
    not_found = call_order_tool("NP-999999")
    check(
        "404 is a non-retryable error",
        not_found["isError"] is True and not_found["isRetryable"] is False and not_found["status"] == 404,
    )

    _call_counts.clear()
    malformed = call_order_tool("100245")
    check(
        "malformed id is a non-retryable 400",
        malformed["isError"] is True and malformed["isRetryable"] is False and malformed["status"] == 400,
    )

    _call_counts.clear()
    first = call_order_tool("NP-100245")
    check(
        "queued 504 is a retryable error",
        first["isError"] is True and first["isRetryable"] is True and first["status"] == 504,
    )
    retried = run_with_retry("NP-100245")
    check("retry loop recovers after the transient error", retried["isError"] is False)

    print(f"\n{'ALL CHECKS PASSED' if failures == 0 else f'{failures} CHECK(S) FAILED'}")
    return failures == 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        ok = self_check()
        sys.exit(0 if ok else 1)

    client = Anthropic()

    print("Case A: NP-100245 (times out once, then succeeds)")
    run_agent_turn(client, "What's the status of my order NP-100245?")

    print("\nCase B: NP-999999 (does not exist)")
    _call_counts.clear()
    run_agent_turn(client, "Can you check on order NP-999999 for me?")

    print("\nCase C: 100245 (malformed — missing the NP- prefix)")
    run_agent_turn(client, "Can you check on order 100245 for me?")
