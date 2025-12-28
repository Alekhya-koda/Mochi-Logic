from __future__ import annotations

BANNED_PHRASES = [
    "diagnose",
    "diagnosis",
    "treatment plan",
    "medical condition",
    "you have",
    "clinical depression",
]


def is_safe(text: str) -> bool:
    lower = text.lower()
    return not any(term in lower for term in BANNED_PHRASES)


def validate_response(text: str) -> tuple[bool, list[str]]:
    issues = [term for term in BANNED_PHRASES if term in text.lower()]
    return len(issues) == 0, issues
