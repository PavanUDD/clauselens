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
    """
    rule_id: str                                    # "RENTAL_R001"
    name: str                                       # Short title
    contract_types: list[str]                       # ["rental"]
    severity: Severity                              # "HIGH"/"MEDIUM"/"LOW"
    category: str                                   # "termination" | "payment" | ...
    detection_patterns: list[str]                   # regex patterns
    plain_english: str                              # one-sentence summary
    explanation_template: str                       # filled with extracted values
    typical_range: str                              # human-readable benchmark
    negotiation_script: str                         # ready-to-send suggestion
    semantic_queries: list[str] = field(default_factory=list)  # for semantic fallback
    threshold_check: Optional[Callable[[dict], bool]] = None   # fine-grained gate
    learn_more: Optional[str] = None                # short educational note


@dataclass
class RiskFlag:
    """What the risk engine returns per triggered rule."""
    rule_id: str
    name: str
    severity: Severity
    category: str
    plain_english: str
    explanation: str            # rendered explanation_template
    negotiation_script: str
    typical_range: str
    evidence: list[dict]        # chunks that matched: [{page_num, text, keywords}]
    match_strength: float       # 0.0 - 0.99, keyword-density heuristic
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