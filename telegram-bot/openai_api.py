import os
from typing import TypedDict, Literal

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


class AiMessage(TypedDict):
    tokens: int
    role: Literal["user", "assistant"]
    content: str


async def next_dialog_message(history: list[AiMessage], request: str) -> str:
    req_approx_tokens = _approx_tokens(request)
    history.append({
        "role": "user",
        "content": request,
        "tokens": req_approx_tokens})
    
    context = _cut_history(history)
    context_tokens = sum(m["tokens"] for m in context) - req_approx_tokens
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=_to_openai_format(context)
    )
    usage = response["usage"]
    prompt_tokens = usage["prompt_tokens"]
    history[-1]["tokens"] = prompt_tokens - context_tokens

    completion_tokens = usage["completion_tokens"]
    completion_message = response["choices"][0]["message"]
    history.append({
        "role": completion_message["role"],
        "content": completion_message["content"],
        "tokens": completion_tokens})

    return completion_message["content"]
    

def _cut_history(history: list[AiMessage], max_tokens=512) -> list[AiMessage]:
    tokens_used = 0
    new_history = []
    for entry in history[::-1]:
        tokens_used += entry["tokens"]
        if tokens_used < max_tokens:
            new_history.insert(0, entry)
        else:
            break
    return new_history

def _to_openai_format(history: list[AiMessage]):
    allowed = {"role", "content"}
    return [{k: v for k, v in m.items() if k in allowed} for m in history]

def _approx_tokens(string: str, tokens_per_word=1.33):
    return len(string.split()) * tokens_per_word
