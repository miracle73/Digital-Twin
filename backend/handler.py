"""AWS Lambda entry point for the digital twin chat API (Function URL).

POST {"message": "...", "history": [{"role": "user"|"assistant", "content": "..."}]}
  -> {"reply": "..."}

Uses only the standard library so the deployment zip needs no dependencies.
"""
import json
import os
import urllib.request

from twin import SYSTEM_PROMPT, tool_functions, tools

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.environ.get("MODEL", "openai/gpt-4o-mini")
MAX_HISTORY = 20


def complete(messages):
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"model": MODEL, "messages": messages, "tools": tools}).encode(),
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=50) as resp:
        return json.load(resp)["choices"][0]["message"]


def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history[-MAX_HISTORY:]:
        if turn.get("role") in ("user", "assistant") and isinstance(turn.get("content"), str):
            messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    reply = complete(messages)
    if reply.get("tool_calls"):
        messages.append(reply)
        for call in reply["tool_calls"]:
            fn = tool_functions.get(call["function"]["name"])
            result = fn() if fn else json.dumps({"error": "Unknown tool"})
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})
        reply = complete(messages)

    return reply.get("content") or ""


def respond(status, body):
    return {"statusCode": status, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return respond(400, {"error": "Invalid JSON"})

    message = str(body.get("message", "")).strip()[:2000]
    if not message:
        return respond(400, {"error": "message is required"})

    try:
        return respond(200, {"reply": chat(message, body.get("history") or [])})
    except Exception as exc:  # surface upstream failures without leaking secrets
        print(f"chat failed: {exc!r}")
        return respond(502, {"error": "Upstream model error"})
