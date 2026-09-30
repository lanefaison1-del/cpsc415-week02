#!/usr/bin/env python3
"""Send one question to a chat model, print the answer, then the model and token usage.

Usage:
    python3 chat.py "In one sentence, what is a context window?"

Environment variables:
    CHAT_BASE_URL       e.g. https://openrouter.ai/api/v1
    CHAT_MODEL          e.g. minimax/minimax-m3
    OPENROUTER_API_KEY  the key (CHAT_API_KEY is used instead when it is set, e.g. for a local model)

Standard library only.
"""

import json
import os
import sys
import urllib.error
import urllib.request

SYSTEM_MESSAGE = (
    "Answer briefly for a college student studying engineering, "
    "not computer science, but who is trying to learn it."
)
MAX_TOKENS = 600  # the lab changes this later to see what a low cap does
TIMEOUT_SECONDS = 120


def fail(message):
    """Print a clear error and exit with a non-zero code."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    # The question: all command-line arguments joined, so quoting is optional.
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        fail('no question given. Usage: python3 chat.py "your question"')

    # Configuration comes only from the environment. Nothing secret is in this file.
    base_url = os.environ.get("CHAT_BASE_URL", "").strip().rstrip("/")
    model = os.environ.get("CHAT_MODEL", "").strip()
    api_key = os.environ.get("CHAT_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not base_url:
        fail("CHAT_BASE_URL is not set.")
    if not model:
        fail("CHAT_MODEL is not set.")
    if not api_key:
        fail("OPENROUTER_API_KEY is not set (or CHAT_API_KEY for a local model).")

    # The request body: this dictionary is exactly the JSON sent to the model.
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": question},
        ],
        "max_tokens": MAX_TOKENS,
    }

    request = urllib.request.Request(
        url=base_url + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )

    # Send it once. No retries, no fallback.
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        fail(f"HTTP {err.code} from the API: {detail}")
    except urllib.error.URLError as err:
        fail(f"could not reach {base_url}: {err.reason}")

    if "error" in data:
        fail(f"the API returned an error: {data['error']}")

    # The answer.
    message = data["choices"][0].get("message") or {}
    answer = (message.get("content") or "").strip()
    print(answer if answer else "(No visible answer. The model may have used its tokens on hidden reasoning.)")

    # The usage: the model that actually answered, and the tokens billed.
    usage = data.get("usage") or {}
    answered_by = data.get("model") or model
    print(
        f"model: {answered_by} | input tokens: {usage.get('prompt_tokens', '?')}"
        f" | output tokens: {usage.get('completion_tokens', '?')}"
    )


if __name__ == "__main__":
    main()
