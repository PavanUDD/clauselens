"""Contract Health Score — 0-100 scalar summarizing overall risk."""
from __future__ import annotations

from clauselens.rulebook.schema import RiskFlag
from config import SEVERITY_WEIGHTS, MAX_HEALTH_SCORE
from clauselens.utils.logger import get_logger

log = get_logger(__name__)


def compute(flags: list[RiskFlag]) -> dict:
    """Compute health score. Returns {score, grade, label, counts}."""
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in flags:
        counts[f.severity] += 1

    penalty = sum(counts[s] * SEVERITY_WEIGHTS[s] for s in counts)
    score = max(0, MAX_HEALTH_SCORE - penalty)

    if score >= 85:
        grade, label = "A", "Low Risk"
    elif score >= 70:
        grade, label = "B", "Moderate Risk"
    elif score >= 50:
        grade, label = "C", "Elevated Risk"
    elif score >= 30:
        grade, label = "D", "High Risk"
    else:
        grade, label = "F", "Severe Risk"

    result = {
        "score": score,
        "grade": grade,
        "label": label,
        "high_flags": counts["HIGH"],
        "medium_flags": counts["MEDIUM"],
        "low_flags": counts["LOW"],
        "total_flags": sum(counts.values()),
    }
    log.info(f"Health score: {score}/100 ({grade} — {label})")
    return result