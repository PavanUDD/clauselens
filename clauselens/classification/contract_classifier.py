"""Detect contract type from its content using keyword signatures."""
from __future__ import annotations
import re
from collections import Counter

from clauselens.utils.logger import get_logger

log = get_logger(__name__)

# Keyword signatures per contract type (lowercase).
# Score = weighted sum of matches. Highest-scoring type wins.
CONTRACT_SIGNATURES: dict[str, dict[str, int]] = {
    "rental": {
        "lease": 5, "tenant": 5, "landlord": 5, "rent": 4, "rental": 4,
        "premises": 3, "security deposit": 5, "sublet": 4, "eviction": 4,
        "lease term": 4, "leased property": 4, "dwelling": 3, "occupancy": 3,
        "monthly rent": 5, "lease agreement": 6, "residential": 3
    },
    "employment": {
        "employee": 5, "employer": 5, "employment": 5, "salary": 4, "wages": 4,
        "compensation": 3, "at-will": 5, "at will": 5, "termination of employment": 5,
        "job title": 3, "position": 2, "benefits": 3, "paid time off": 4, "pto": 3,
        "non-compete": 5, "noncompete": 5, "severance": 4, "offer letter": 5,
        "work for hire": 4, "probationary period": 4
    },
    "freelance": {
        "contractor": 5, "independent contractor": 6, "freelance": 5, "freelancer": 5,
        "scope of work": 5, "sow": 3, "deliverable": 4, "milestone": 4,
        "client": 3, "project": 2, "consulting": 4, "consultant": 4,
        "statement of work": 5, "hourly rate": 4
    },
    "saas": {
        "service": 2, "saas": 6, "software as a service": 6, "subscription": 5,
        "uptime": 5, "sla": 5, "service level agreement": 6, "api": 3,
        "user account": 3, "platform": 2, "subscription fee": 5, "monthly subscription": 5,
        "annual subscription": 5, "cloud service": 4, "data processing": 3
    },
    "loan": {
        "borrower": 5, "lender": 5, "loan": 5, "principal amount": 5,
        "interest rate": 5, "apr": 4, "promissory note": 6, "repayment": 4,
        "default": 3, "collateral": 5, "amortization": 5, "maturity date": 5,
        "prepayment": 4, "loan agreement": 6
    }
}


def classify(chunks: list[dict]) -> tuple[str, float, dict[str, int]]:
    """Classify contract type. Returns (type, confidence 0-1, raw_scores)."""
    if not chunks:
        return "unknown", 0.0, {}

    full_text = " ".join(c["text"] for c in chunks).lower()
    scores: dict[str, int] = {}
    for ctype, keywords in CONTRACT_SIGNATURES.items():
        total = 0
        for kw, weight in keywords.items():
            pattern = r"\b" + re.escape(kw) + r"\b"
            matches = len(re.findall(pattern, full_text))
            total += matches * weight
        scores[ctype] = total

    log.info(f"Contract classification scores: {scores}")

    if not scores or max(scores.values()) < 10:
        return "unknown", 0.0, scores

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]
    sorted_scores = sorted(scores.values(), reverse=True)
    # confidence = margin between winner and runner-up, normalized
    if len(sorted_scores) > 1 and best_score > 0:
        margin = (best_score - sorted_scores[1]) / best_score
        confidence = round(min(0.5 + margin * 0.5, 0.99), 2)
    else:
        confidence = 0.5

    log.info(f"Classified as: {best_type} (confidence {confidence})")
    return best_type, confidence, scores