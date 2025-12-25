from __future__ import annotations

import os
from typing import Any

from openai import AsyncOpenAI

from ..policy.redaction import redact
from ..policy.validator import validate_response


SYSTEM_PROMPT = (
    "You are a calm, compassionate support companion for expecting and new parents. "
    "Acknowledge effort and emotions first, with warm, natural phrasing (e.g., "
    "'It sounds like you’re trying really hard,' 'That feels heavy,' 'Would it feel okay if…'). "
    "Avoid clinical wording or commands; keep guidance gentle, collaborative, and validating. "
    "Listen before problem-solving; ask only one simple clarifying question at a time. "
    "Keep replies short and conversational (aim for 4–6 sentences), and stay non-clinical with no medical claims."
)


class LLMOrchestrator:
    def __init__(self, client: AsyncOpenAI | None = None, model: str | None = None):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = client or AsyncOpenAI(api_key=api_key)
        self.model = model or "gpt-5.2"

    async def respond(self, user_message: str, context: list[dict[str, str]] | None = None) -> dict[str, Any]:
        safe_user_message = redact(user_message)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": safe_user_message})

        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_completion_tokens=220,
        )

        content = completion.choices[0].message.content or ""
        is_ok, issues = validate_response(content)
        if not is_ok:
            fallback = (
                "I want to stay respectful and avoid clinical language. "
                "It sounds like you're going through a lot—I'm here to help you reflect "
                "and understand what you're feeling without giving medical advice."
            )
            content = fallback
        return {
            "content": content,
            "raw_response": completion.model_dump(),
            "issues": issues if not is_ok else [],
        }
