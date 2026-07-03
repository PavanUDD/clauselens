"""Rulebook schema — every rule follows this structure."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional, Literal

Severity = Literal["HIGH", "MEDIUM", "LOW"]


@dataclass
class Rule:
    """A single contract risk rule.

    Detection = two-stage:
      1. `detection_patterns` (regex) must match at least one chunk.
      2. Optional `threshold_check(terms)` — fine-grained numeric check
         (e.g., "deposit > 2 months rent"). Return True to trigger.
      3. Optional `safe_harbor_patterns` (regex) — if ANY of these match in
         the SAME chunk as the detection pattern, the rule is either skipped
         entirely (safe_harbor_skips=True) or downgraded to LOW severity.
         Use for clauses that are only risky when protective language is ABSENT.
    """
    rule_id: str
    name: str
    contract_types: list[str]
    severity: Severity
    category: str
    detection_patterns: list[str]
    plain_english: str
    explanation_template: str
    typical_range: str
    negotiation_script: str
    semantic_queries: list[str] = field(default_factory=list)
    threshold_check: Optional[Callable[[dict], bool]] = None
    # --- Safe harbor ---
    safe_harbor_patterns: list[str] = field(default_factory=list)
    # True  = skip the flag entirely (clause is actually fine)
    # False = downgrade severity to LOW and surface a softer note
    safe_harbor_skips: bool = False
    safe_harbor_note: str = ""   # replaces plain_english when downgraded (not skipped)
    learn_more: Optional[str] = None


@dataclass
class RiskFlag:
    """What the risk engine returns per triggered rule."""
    rule_id: str
    name: str
    severity: Severity
    category: str
    plain_english: str
    explanation: str
    negotiation_script: str
    typical_range: str
    evidence: list[dict]
    match_strength: float
    learn_more: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "severity": self.severity,
            "category": self.category,
            "plain_english": self.plain_english,
            "explanation": self.explanation,
            "negotiation_script": self.negotiation_script,
            "typical_range": self.typical_range,
            "evidence": self.evidence,
            "match_strength": self.match_strength,
            "learn_more": self.learn_more,
        }