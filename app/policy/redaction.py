from __future__ import annotations

import re


SENSITIVE_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"),
    re.compile(r"\\b\\d{3}-\\d{2}-\\d{4}\\b"),
]


def redact(text: str) -> str:
    redacted = text
    for pattern in SENSITIVE_PATTERNS:
        redacted = pattern.sub("[redacted]", redacted)
    return redacted
