"""Tests for term extractor (money, percentages, durations)."""
from clauselens.analysis.term_extractor import (
    extract_money, extract_percentages, extract_durations,
    duration_to_days, extract_all_terms,
)


def test_extract_money_simple(sample_text_with_money):
    amounts = extract_money(sample_text_with_money)
    assert 50000.0 in amounts
    assert 1200.0 in amounts
    assert 500.0 in amounts


def test_extract_money_no_match():
    assert extract_money("no money in this text") == []


def test_extract_percentages(sample_text_with_percentages):
    pcts = extract_percentages(sample_text_with_percentages)
    assert 5.0 in pcts
    assert 10.0 in pcts
    assert 1.5 in pcts


def test_extract_durations(sample_text_with_durations):
    durations = extract_durations(sample_text_with_durations)
    units = [u for _, u in durations]
    assert "month" in units
    assert "day" in units


def test_duration_to_days():
    assert duration_to_days(1, "year") == 365
    assert duration_to_days(2, "months") == 60
    assert duration_to_days(7, "days") == 7
    assert duration_to_days(1, "week") == 7


def test_extract_all_terms_full(rental_chunks):
    terms = extract_all_terms(rental_chunks)
    assert terms["money_count"] >= 2
    assert terms["max_money"] is not None
    assert terms["max_money"] >= 1800