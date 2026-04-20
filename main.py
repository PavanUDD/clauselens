"""ClauseLens CLI — full contract analysis pipeline.

Usage:
    python main.py --pdf path/to/contract.pdf
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

from clauselens.ingestion.pdf_loader import load_pdf
from clauselens.ingestion.chunker import split_into_chunks
from clauselens.classification.contract_classifier import classify
from clauselens.retrieval.search import build_index
from clauselens.analysis.term_extractor import extract_all_terms
from clauselens.analysis.risk_engine import evaluate
from clauselens.analysis.health_score import compute as compute_health
from clauselens.analysis.summarizer import summarize
from clauselens.utils.logger import get_logger
from config import STORAGE_DIR

log = get_logger("main")


def run_full_analysis(pdf_path: str, save_json: bool = True) -> dict:
    pdf_path = Path(pdf_path)
    print(f"\n{'='*70}")
    print(f"  ClauseLens — Analyzing: {pdf_path.name}")
    print(f"{'='*70}\n")

    # 1. Load PDF
    pages = load_pdf(pdf_path)
    print(f"✓ Loaded {len(pages)} pages")

    # 2. Chunk
    chunks = split_into_chunks(pages)
    print(f"✓ Created {len(chunks)} chunks")

    # 3. Classify contract type
    contract_type, confidence, scores = classify(chunks)
    print(f"✓ Classified as: {contract_type.upper()} (confidence: {confidence})")

    # 4. Build FAISS index (in-memory)
    index, chunks = build_index(chunks)
    print(f"✓ Built FAISS index: {index.ntotal} vectors")

    # 5. Extract terms (money, %, durations, dates)
    terms = extract_all_terms(chunks)
    print(f"✓ Extracted terms: {terms['money_count']} $ amounts, "
          f"{terms['percentage_count']} percentages, "
          f"{terms['duration_count']} durations")

    # 6. Run risk engine
    flags = evaluate(chunks, contract_type, terms)
    print(f"✓ Risk engine: {len(flags)} flags triggered")

    # 7. Health score
    health = compute_health(flags)

    # 8. Plain-English summary
    summary = summarize(contract_type, terms, flags, health)

    # --- PRINT REPORT ---
    print(f"\n{'='*70}")
    print(f"  CONTRACT HEALTH SCORE: {health['score']}/100  (Grade {health['grade']} — {health['label']})")
    print(f"{'='*70}")
    print(f"  🔴 HIGH: {health['high_flags']}   🟡 MEDIUM: {health['medium_flags']}   🟢 LOW: {health['low_flags']}")

    print(f"\n{'='*70}")
    print("  PLAIN-ENGLISH SUMMARY")
    print(f"{'='*70}")
    print(summary.replace("**", ""))  # strip markdown bold for CLI

    print(f"\n{'='*70}")
    print("  DETAILED RISK FLAGS")
    print(f"{'='*70}")
    if not flags:
        print("  No risks detected against the rulebook for this contract type.")
    for i, f in enumerate(flags, 1):
        sev_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[f.severity]
        print(f"\n  [{i}] {sev_icon} [{f.severity}] {f.name}")
        print(f"      Plain English : {f.plain_english}")
        print(f"      Typical Range : {f.typical_range}")
        print(f"      Match Strength: {f.match_strength}")
        if f.evidence:
            top = f.evidence[0]
            print(f"      Evidence (pg {top['page_num']}): \"{top['text'][:200]}...\"")
        print(f"      💬 Suggested: {f.negotiation_script[:150]}...")

    # --- SAVE JSON ---
    if save_json:
        doc_id = pdf_path.stem.replace(" ", "_")
        output = {
            "doc_id": doc_id,
            "pdf_name": pdf_path.name,
            "contract_type": contract_type,
            "classification_confidence": confidence,
            "classification_scores": scores,
            "pages": len(pages),
            "chunks": len(chunks),
            "terms": terms,
            "health": health,
            "flags": [f.to_dict() for f in flags],
            "summary": summary,
        }
        out_path = STORAGE_DIR / f"{doc_id}_analysis.json"
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(output, fh, indent=2, default=str)
        print(f"\n✓ Full analysis saved to: {out_path}\n")
        return output

    return {}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ClauseLens — contract risk analyzer")
    parser.add_argument("--pdf", required=True, help="Path to contract PDF")
    parser.add_argument("--no-save", action="store_true", help="Skip saving JSON output")
    args = parser.parse_args()

    try:
        run_full_analysis(args.pdf, save_json=not args.no_save)
    except FileNotFoundError as e:
        print(f"\n❌ {e}\n"); sys.exit(1)
    except Exception as e:
        log.exception("Analysis failed")
        print(f"\n❌ Analysis failed: {e}\n"); sys.exit(1)