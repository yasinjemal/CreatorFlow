from __future__ import annotations
from typing import Dict, List

NEGATIVE_PATTERNS = [
    "clickbait",
    "ALL CAPS",
]


def analyze_tone(text: str, brand_voice: str) -> Dict[str, object]:
    issues: List[str] = []
    score = 90
    if any(word in text for word in ["FREE!!!", "BUY NOW!!!"]):
        issues.append("Aggressive sales language detected")
        score -= 20
    for pat in NEGATIVE_PATTERNS:
        if pat.lower() in text.lower():
            issues.append(f"Discouraged pattern: {pat}")
            score -= 10
    if len(text.split()) < 5:
        issues.append("Too short; lacks substance")
        score -= 15
    return {"score": max(score, 0), "issues": issues, "summary": f"Tone aligned ~{max(score,0)}% with '{brand_voice}'"}
