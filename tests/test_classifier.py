"""Tests for contract classifier."""
import pytest
from clauselens.classification.contract_classifier import classify


def test_classify_rental(rental_chunks):
    ctype, confidence, scores = classify(rental_chunks)
    assert ctype == "rental"
    assert confidence > 0.5
    assert scores["rental"] > scores.get("employment", 0)


def test_classify_employment(employment_chunks):
    ctype, confidence, scores = classify(employment_chunks)
    assert ctype == "employment"
    assert confidence > 0.5


def test_classify_empty_chunks():
    ctype, confidence, scores = classify([])
    assert ctype == "unknown"
    assert confidence == 0.0


def test_classify_unknown_text():
    chunks = [{
        "chunk_id": 0, "page_num": 1,
        "text": "The quick brown fox jumps over the lazy dog. Lorem ipsum dolor sit amet.",
    }]
    ctype, confidence, scores = classify(chunks)
    assert ctype == "unknown"
    assert confidence == 0.0


def test_classify_returns_all_scores(rental_chunks):
    _, _, scores = classify(rental_chunks)
    expected_types = {"rental", "employment", "freelance", "saas", "loan"}
    assert expected_types.issubset(set(scores.keys()))