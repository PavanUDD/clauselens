"""Semantic chunker with overlap."""
import json
from pathlib import Path
from clauselens.utils.logger import get_logger
from config import CHUNK_SIZE, CHUNK_OVERLAP

log = get_logger(__name__)

def split_into_chunks(pages: list[dict],
                      chunk_size: int = CHUNK_SIZE,
                      overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """Split pages into overlapping word-based chunks."""
    chunks = []
    chunk_id = 0
    for page in pages:
        words = page["text"].split()
        if not words:
            continue
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            text = " ".join(words[start:end])
            chunks.append({
                "chunk_id": chunk_id,
                "page_num": page["page_num"],
                "text": text,
                "word_count": end - start
            })
            chunk_id += 1
            if end == len(words):
                break
            start += chunk_size - overlap
    log.info(f"Created {len(chunks)} chunks from {len(pages)} pages")
    return chunks

def save_chunks(chunks: list[dict], path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
    log.info(f"Saved {len(chunks)} chunks → {path}")