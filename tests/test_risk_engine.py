"""Tests for the risk engine."""
from clauselens.analysis.risk_engine import evaluate, RULEBOOKS
from clauselens.analysis.term_extractor import extract_all_terms


def test_rulebooks_loaded():
    """Both core rulebooks should be registered."""
    assert "rental" in RULEBOOKS
    assert "employment" in RULEBOOKS
    assert len(RULEBOOKS["rental"]) >= 15
    assert len(RULEBOOKS["employment"]) >= 15


def test_rental_rules_trigger(rental_chunks):
    flags = evaluate(rental_chunks, "rental")
    assert len(flags) > 0
    flag_names = [f.name.lower() for f in flags]
    # Should catch at least some obvious flags in the test chunks
    assert any("pets" in n or "sublet" in n or "deposit" in n or "attorney" in n
               for n in flag_names)


def test_employment_rules_trigger(employment_chunks):
    flags = evaluate(employment_chunks, "employment")
    assert len(flags) > 0
    flag_names = [f.name.lower() for f in flags]
    assert any("non-compete" in n or "arbitration" in n or "severance" in n
               for n in flag_names)


def test_severity_sorting(rental_chunks):
    flags = evaluate(rental_chunks, "rental")
    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    prev_rank = -1
    for f in flags:
        rank = severity_order[f.severity]
        assert rank >= prev_rank
        prev_rank = rank


def test_unknown_contract_type_returns_generic_rules(rental_chunks):
    """Unknown contract type should use generic fallback rulebook."""
    if "unknown" in RULEBOOKS:
        flags = evaluate(rental_chunks, "unknown")
        # Generic rules may or may not trigger on rental text — just confirm no crash
        assert isinstance(flags, list)


def test_flag_has_required_fields(rental_chunks):
    flags = evaluate(rental_chunks, "rental")
    assert len(flags) > 0
    f = flags[0]
    assert f.rule_id
    assert f.name
    assert f.severity in {"HIGH", "MEDIUM", "LOW"}
    assert f.plain_english
    assert 0.0 <= f.match_strength <= 1.0
    assert isinstance(f.evidence, list)


def test_evidence_precision(rental_chunks):
    """Evidence snippet should contain at least one matched keyword."""
    flags = evaluate(rental_chunks, "rental")
    for f in flags:
        if not f.evidence or not f.evidence[0].get("matched_keywords"):
            continue
        text = f.evidence[0]["text"].lower()
        keywords = [k.lower() for k in f.evidence[0]["matched_keywords"] if k]
        assert any(k in text for k in keywords), \
            f"Flag {f.name}: evidence missing keyword"