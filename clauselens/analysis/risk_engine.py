"""Risk engine — evaluates rulebook against contract chunks.

Features:
- Negation-aware matching (skips "no rent increase" false positives)
- Safe harbor matching (downgrades/skips rules when protective language is found)
- Deposit threshold check (only flags deposit if > 2x monthly rent)
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
from clauselens.rulebook.nda_rules import NDA_RULES
from clauselens.rulebook.vendor_rules import VENDOR_RULES
from clauselens.rulebook.staffing_rules import STAFFING_RULES
from clauselens.utils.logger import get_logger

log = get_logger(__name__)

RULEBOOKS: dict[str, list[Rule]] = {
    "rental":     RENTAL_RULES,
    "employment": EMPLOYMENT_RULES,
    "freelance":  FREELANCE_RULES,
    "saas":       SAAS_RULES,
    "loan":       LOAN_RULES,
    "nda":        NDA_RULES,
    "vendor":     VENDOR_RULES,
    "staffing":   STAFFING_RULES,
    "unknown":    GENERIC_RULES,
}

# Negation phrases that INVALIDATE a match if found right before the keyword
NEGATION_RE = re.compile(
    r"\b(?:no|not|never|without|cannot|shall\s+not|will\s+not|may\s+not|"
    r"there\s+(?:will|shall)\s+be\s+no|there\s+are\s+no|is\s+not|are\s+not)\b",
    re.IGNORECASE,
)

# Rules where negation IS the concern — don't filter them out
NEGATION_IS_THE_POINT = {
    "RENTAL_R005",   # No subletting
    "RENTAL_R009",   # No pets
    "RENTAL_R015",   # No guests
    "RENTAL_R008",
    "EMP_R003",      # No severance
    "EMP_R008",      # No overtime
    "VENDOR_R016",   # No cap on liability / no obligation to carry insurance
}


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


def _check_safe_harbor(rule: Rule, evidence: list[dict]) -> bool:
    """
    Returns True if safe harbor language is found in ANY of the matching chunks.
    Safe harbor = the clause already contains the protection we were worried about.
    Example: landlord entry clause that explicitly requires 24-hour notice.
    """
    if not rule.safe_harbor_patterns:
        return False

    harbor_re = re.compile(
        "|".join(rule.safe_harbor_patterns), re.IGNORECASE
    )

    for chunk in evidence:
        # Check against the full chunk text, not just the snippet,
        # so notice language that appears near (but not inside) the snippet still counts
        full_text = chunk.get("full_chunk", chunk["text"])
        if harbor_re.search(full_text):
            return True

    return False


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

        # --- Numeric threshold gate (e.g. deposit amount check) ---
        if rule.threshold_check and terms:
            try:
                if not rule.threshold_check(terms):
                    log.debug(f"{rule.rule_id} skipped — threshold not met")
                    continue
            except Exception as e:
                log.warning(f"Threshold check failed for {rule.rule_id}: {e}")

        # --- Safe harbor check ---
        harbor_found = _check_safe_harbor(rule, evidence)
        if harbor_found:
            if rule.safe_harbor_skips:
                # Clause is genuinely fine — drop the flag entirely
                log.debug(f"{rule.rule_id} skipped — safe harbor language found")
                continue
            else:
                # Clause exists but has protection — downgrade to LOW
                effective_severity = "LOW"
                effective_plain_english = (
                    rule.safe_harbor_note
                    if rule.safe_harbor_note
                    else f"✅ This clause appears to include standard protections. {rule.plain_english}"
                )
        else:
            effective_severity = rule.severity
            effective_plain_english = rule.plain_english

        match_strength = round(min(0.5 + len(evidence) * 0.1, 0.99), 2)

        flags.append(RiskFlag(
            rule_id=rule.rule_id,
            name=rule.name,
            severity=effective_severity,
            category=rule.category,
            plain_english=effective_plain_english,
            explanation=_render_explanation(rule, evidence),
            negotiation_script=rule.negotiation_script,
            typical_range=rule.typical_range,
            evidence=evidence[:3],
            match_strength=match_strength,
            learn_more=rule.learn_more,
        ))

    # --- Unknown clause detection ---
    # Track which chunks were matched by at least one rule
    matched_chunk_ids = set()
    for flag in flags:
        for evidence in flag.evidence:
            matched_chunk_ids.add(evidence["chunk_id"])

    # Flag chunks that matched NO rules and are long enough to matter
    unmatched = [
        c for c in chunks
        if c["chunk_id"] not in matched_chunk_ids
        and len(c["text"].split()) > 40
        and not any(skip in c["text"].lower() for skip in [
            "table of contents",
            "article i",
            "article ii",
            "section 1.",
            "section 2.",
            "........",
            "exhibit",
            "schedule",
        ])
    ]

    if unmatched:
        sample = unmatched[0]
        flags.append(RiskFlag(
            rule_id="UNKNOWN_CLAUSE",
            name="Unusual clause — legal review recommended",
            severity="LOW",
            category="unknown",
            plain_english=(
                "One or more clauses in this contract didn't match our "
                "standard risk patterns. This doesn't mean they're safe — "
                "it means they're unusual. We recommend reviewing these "
                "sections with a legal professional before signing."
            ),
            explanation=(
                f"We detected {len(unmatched)} clause(s) outside our "
                f"standard rulebook. Sample clause starts at page "
                f"{sample['page_num']}. These may be standard for your "
                f"industry or genuinely unusual — a professional can confirm."
            ),
            negotiation_script=(
                "Before signing, ask your attorney to review the flagged "
                "sections. Ask specifically: 'Is this clause standard for "
                "this type of agreement in our industry?'"
            ),
            typical_range="All clauses should be explainable in plain English",
            evidence=[{
                "chunk_id": c["chunk_id"],
                "page_num": c["page_num"],
                "text": c["text"][:300] + "..." if len(c["text"]) > 300 else c["text"],
                "full_chunk": c["text"],
                "matched_keywords": [],
                "hit_count": 0,
            } for c in unmatched[:2]],
            match_strength=0.0,
            learn_more="ClauseLens flags unknown clauses rather than guessing — trust requires honesty.",
        ))

    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    flags.sort(key=lambda f: (severity_order[f.severity], -f.match_strength))

    log.info(f"Risk engine: {len(flags)} flags triggered for {contract_type}")
    return flags