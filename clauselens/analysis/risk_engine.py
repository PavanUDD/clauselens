"""Risk engine — evaluates rulebook against contract chunks.

Features:
- Negation-aware matching (skips "no rent increase" false positives)
- Precise snippet extraction centered on the actual regex hit
- Works on ANY contract — no PDF-specific logic
"""
from __future__ import annotations
import re

from clauselens.rulebook.schema import Rule, RiskFlag
from clauselens.rulebook.rental_rules import RENTAL_RULES
from clauselens.rulebook.employment_rules import EMPLOYMENT_RULES
from clauselens.rulebook.freelance_rules import FREELANCE_RULES
from clauselens.rulebook.saas_rules import SAAS_RULES
from clauselens.rulebook.loan_rules import LOAN_RULES
from clauselens.rulebook.generic_rules import GENERIC_RULES
from clauselens.utils.logger import get_logger

log = get_logger(__name__)

RULEBOOKS: dict[str, list[Rule]] = {
    "rental": RENTAL_RULES,
    "employment": EMPLOYMENT_RULES,
    "freelance": FREELANCE_RULES,
    "saas": SAAS_RULES,
    "loan": LOAN_RULES,
    "unknown": GENERIC_RULES,
}

# Negation phrases that INVALIDATE a match if found right before the keyword
# (e.g., "no rent increase", "shall not increase")
NEGATION_RE = re.compile(
    r"\b(?:no|not|never|without|cannot|shall\s+not|will\s+not|may\s+not|"
    r"there\s+(?:will|shall)\s+be\s+no|there\s+are\s+no|is\s+not|are\s+not)\b",
    re.IGNORECASE,
)

# Rules where negation IS the concern — don't filter them out
# (e.g., "no pets" — the restriction itself is the red flag)
NEGATION_IS_THE_POINT = {
    "RENTAL_R005",   # No subletting
    "RENTAL_R009",   # No pets
    "RENTAL_R015",   # No guests
    "EMP_R003",      # No severance
    "EMP_R008",      # No overtime
}


def _flatten(items):
    for item in items:
        if isinstance(item, tuple):
            for sub in item:
                yield sub
        else:
            yield item


def _is_negated(text: str, match_start: int, window: int = 50) -> bool:
    """True if a negation word appears within `window` chars before the match."""
    prefix = text[max(0, match_start - window):match_start]
    return bool(NEGATION_RE.search(prefix))


def _extract_snippet(text: str, match_start: int, match_end: int,
                     before: int = 120, after: int = 230) -> str:
    """Precise snippet centered on the regex hit."""
    start = max(0, match_start - before)
    end = min(len(text), match_end + after)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def _match_rule(rule: Rule, chunks: list[dict]) -> list[dict]:
    """Run rule's regex patterns. Return matching chunks with precise snippets."""
    combined = re.compile("|".join(rule.detection_patterns), re.IGNORECASE)
    check_negation = rule.rule_id not in NEGATION_IS_THE_POINT
    matches = []

    for chunk in chunks:
        text = chunk["text"]
        valid_hits = list(combined.finditer(text))

        if check_negation:
            valid_hits = [m for m in valid_hits if not _is_negated(text, m.start())]

        if not valid_hits:
            continue

        # Snippet comes from the FIRST valid hit — guarantees evidence matches flag
        first = valid_hits[0]
        snippet = _extract_snippet(text, first.start(), first.end())

        keywords = list({m.group(0).lower().strip() for m in valid_hits})

        matches.append({
            "chunk_id": chunk["chunk_id"],
            "page_num": chunk["page_num"],
            "text": snippet,
            "full_chunk": text,
            "matched_keywords": keywords,
            "hit_count": len(valid_hits),
        })

    matches.sort(key=lambda m: m["hit_count"], reverse=True)
    return matches


def _render_explanation(rule: Rule, evidence: list[dict]) -> str:
    pages = sorted({e["page_num"] for e in evidence})
    pages_str = ", ".join(str(p) for p in pages)
    try:
        return rule.explanation_template.format(pages=pages_str)
    except (KeyError, IndexError):
        return rule.explanation_template


def evaluate(chunks: list[dict],
             contract_type: str,
             terms: dict | None = None) -> list[RiskFlag]:
    """Run all rules for the contract type. Return triggered RiskFlags."""
    rules = RULEBOOKS.get(contract_type, [])
    if not rules:
        log.warning(f"No rulebook for contract type: {contract_type}")
        return []

    flags: list[RiskFlag] = []
    for rule in rules:
        evidence = _match_rule(rule, chunks)
        if not evidence:
            continue

        if rule.threshold_check and terms:
            try:
                if not rule.threshold_check(terms):
                    continue
            except Exception as e:
                log.warning(f"Threshold check failed for {rule.rule_id}: {e}")

        match_strength = round(min(0.5 + len(evidence) * 0.1, 0.99), 2)

        flags.append(RiskFlag(
            rule_id=rule.rule_id,
            name=rule.name,
            severity=rule.severity,
            category=rule.category,
            plain_english=rule.plain_english,
            explanation=_render_explanation(rule, evidence),
            negotiation_script=rule.negotiation_script,
            typical_range=rule.typical_range,
            evidence=evidence[:3],
            match_strength=match_strength,
            learn_more=rule.learn_more,
        ))

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    flags.sort(key=lambda f: (severity_order[f.severity], -f.match_strength))

    log.info(f"Risk engine: {len(flags)} flags triggered for {contract_type}")
    return flags