"""Extract specific values from contract text: money, percentages, durations, dates."""
from __future__ import annotations
import re

from clauselens.utils.logger import get_logger

log = get_logger(__name__)

# --- Regex patterns ---
MONEY_RE = re.compile(
    r"\$\s?([\d,]+(?:\.\d{1,2})?)\b|\b([\d,]+(?:\.\d{1,2})?)\s+dollars?\b",
    re.IGNORECASE
)
PERCENT_RE = re.compile(r"(\d+(?:\.\d+)?)\s?%|\b(\d+(?:\.\d+)?)\s+percent\b", re.IGNORECASE)
DURATION_RE = re.compile(
    r"\b(\d+)\s+(day|days|week|weeks|month|months|year|years)\b", re.IGNORECASE
)
DATE_RE = re.compile(
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b|"
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
    re.IGNORECASE
)


def _to_float(s: str) -> float:
    return float(s.replace(",", ""))


def extract_money(text: str) -> list[float]:
    """Return all dollar amounts in text."""
    amounts = []
    for m in MONEY_RE.findall(text):
        val = m[0] or m[1]
        if val:
            try:
                amounts.append(_to_float(val))
            except ValueError:
                pass
    return amounts


def extract_percentages(text: str) -> list[float]:
    pcts = []
    for m in PERCENT_RE.findall(text):
        val = m[0] or m[1]
        if val:
            try:
                pcts.append(float(val))
            except ValueError:
                pass
    return pcts


def extract_durations(text: str) -> list[tuple[int, str]]:
    """Return list of (number, unit) tuples."""
    results = []
    for num, unit in DURATION_RE.findall(text):
        try:
            results.append((int(num), unit.lower().rstrip("s")))
        except ValueError:
            pass
    return results


def duration_to_days(num: int, unit: str) -> int:
    """Normalize a duration to days."""
    unit = unit.rstrip("s").lower()
    return {"day": 1, "week": 7, "month": 30, "year": 365}.get(unit, 0) * num


def extract_dates(text: str) -> list[str]:
    return DATE_RE.findall(text)


def extract_all_terms(chunks: list[dict]) -> dict:
    """Run all extractors across all chunks. Returns aggregated terms."""
    all_text = " ".join(c["text"] for c in chunks)
    money = extract_money(all_text)
    pcts = extract_percentages(all_text)
    durations = extract_durations(all_text)
    dates = extract_dates(all_text)

    terms = {
        "money_amounts": sorted(set(money)),
        "max_money": max(money) if money else None,
        "percentages": sorted(set(pcts)),
        "max_percentage": max(pcts) if pcts else None,
        "durations": [f"{n} {u}" for n, u in durations],
        "max_duration_days": max((duration_to_days(n, u) for n, u in durations), default=0),
        "dates": dates[:10],  # first 10 dates
        "money_count": len(money),
        "percentage_count": len(pcts),
        "duration_count": len(durations),
    }
    log.info(f"Terms extracted: {len(money)} money, {len(pcts)} pct, {len(durations)} durations, {len(dates)} dates")
    return terms