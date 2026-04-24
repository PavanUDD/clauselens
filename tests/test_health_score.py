"""Tests for health score computation."""
from clauselens.analysis.health_score import compute
from clauselens.rulebook.schema import RiskFlag


def _mk_flag(severity: str) -> RiskFlag:
    return RiskFlag(
        rule_id="TEST",
        name="test flag",
        severity=severity,
        category="test",
        plain_english="test",
        explanation="test",
        negotiation_script="test",
        typical_range="test",
        evidence=[],
        match_strength=0.5,
    )


def test_perfect_score_no_flags():
    result = compute([])
    assert result["score"] == 100
    assert result["grade"] == "A"


def test_score_decreases_with_flags():
    no_flags = compute([])
    one_high = compute([_mk_flag("HIGH")])
    two_high = compute([_mk_flag("HIGH"), _mk_flag("HIGH")])
    assert no_flags["score"] > one_high["score"] > two_high["score"]


def test_high_penalty_greater_than_low():
    one_high = compute([_mk_flag("HIGH")])
    one_low = compute([_mk_flag("LOW")])
    assert one_high["score"] < one_low["score"]


def test_score_bounds():
    many = [_mk_flag("HIGH") for _ in range(20)]
    result = compute(many)
    assert result["score"] >= 0
    assert result["score"] <= 100


def test_grade_thresholds():
    assert compute([])["grade"] == "A"  # 100
    # HIGH = 15, so 2 HIGH = 70 → Grade B
    assert compute([_mk_flag("HIGH"), _mk_flag("HIGH")])["grade"] == "B"


def test_counts_by_severity():
    flags = [_mk_flag("HIGH"), _mk_flag("MEDIUM"), _mk_flag("MEDIUM"), _mk_flag("LOW")]
    result = compute(flags)
    assert result["high_flags"] == 1
    assert result["medium_flags"] == 2
    assert result["low_flags"] == 1
    assert result["total_flags"] == 4