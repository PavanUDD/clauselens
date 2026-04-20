"""FAISS-based semantic search with cached embedding model."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from clauselens.utils.logger import get_logger
from config import EMBEDDING_MODEL, DEFAULT_TOP_K, MIN_SIMILARITY_SCORE

log = get_logger(__name__)

_model: Optional[SentenceTransformer] = None


def get_model() -> SentenceTransformer:
    """Lazy-load the embedding model. Cached after first call."""
    global _model
    if _model is None:
        log.info(f"Loading embedding model: {EMBEDDING_MODEL} (first load ~30s)")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        log.info("Embedding model ready")
    return _model


def build_index(chunks: list[dict]) -> tuple[faiss.Index, list[dict]]:
    """Build an in-memory FAISS index from chunks. Privacy-first: no disk writes."""
    if not chunks:
        raise ValueError("Cannot build index from empty chunks")

    model = get_model()
    texts = [c["text"] for c in chunks]
    log.info(f"Embedding {len(texts)} chunks")
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    embeddings = embeddings.astype(np.float32)
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    log.info(f"FAISS index built: {index.ntotal} vectors, dim={dim}")
    return index, chunks


def search(query: str,
           index: faiss.Index,
           chunks: list[dict],
           top_k: int = DEFAULT_TOP_K,
           min_score: float = MIN_SIMILARITY_SCORE) -> list[dict]:
    """Semantic search. Returns top_k chunks above min_score."""
    if not query.strip():
        return []
    model = get_model()
    q_vec = model.encode([query], convert_to_numpy=True).astype(np.float32)
    faiss.normalize_L2(q_vec)
    scores, indices = index.search(q_vec, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1 or float(score) < min_score:
            continue
        chunk = chunks[idx]
        results.append({
            "chunk_id": chunk["chunk_id"],
            "page_num": chunk["page_num"],
            "score": round(float(score), 4),
            "text": chunk["text"]
        })
    return results


def search_batch(queries: list[str],
                 index: faiss.Index,
                 chunks: list[dict],
                 top_k: int = DEFAULT_TOP_K) -> dict[str, list[dict]]:
    """Run multiple queries. Used by clause_extractor and question_library."""
    return {q: search(q, index, chunks, top_k) for q in queries}