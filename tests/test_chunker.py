"""Tests for the chunker."""
from clauselens.ingestion.chunker import split_into_chunks


def test_chunker_basic():
    pages = [
        {"page_num": 1, "text": "word " * 500},
        {"page_num": 2, "text": "text " * 300},
    ]
    chunks = split_into_chunks(pages, chunk_size=180, overlap=40)
    assert len(chunks) > 1
    assert all("chunk_id" in c for c in chunks)
    assert all("page_num" in c for c in chunks)
    assert all("text" in c for c in chunks)


def test_chunker_preserves_page_numbers():
    pages = [
        {"page_num": 5, "text": "word " * 100},
        {"page_num": 7, "text": "word " * 100},
    ]
    chunks = split_into_chunks(pages)
    pages_seen = {c["page_num"] for c in chunks}
    assert 5 in pages_seen
    assert 7 in pages_seen


def test_chunker_empty_pages():
    assert split_into_chunks([]) == []


def test_chunker_skips_empty_text():
    pages = [
        {"page_num": 1, "text": ""},
        {"page_num": 2, "text": "real content here"},
    ]
    chunks = split_into_chunks(pages)
    assert len(chunks) == 1
    assert chunks[0]["page_num"] == 2


def test_chunker_unique_chunk_ids():
    pages = [{"page_num": 1, "text": "word " * 1000}]
    chunks = split_into_chunks(pages, chunk_size=180, overlap=40)
    ids = [c["chunk_id"] for c in chunks]
    assert len(ids) == len(set(ids))