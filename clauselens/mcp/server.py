import json
import os
import sys
from flask import Flask, request, jsonify

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.pdf_loader import load_pdf
from ingestion.chunker import split_into_chunks, save_chunks, load_chunks
from retrieval.search import build_index, load_index, search
from analysis.clause_extractor import extract_clauses
from analysis.risk_detector import detect_risks

app = Flask(__name__)

INDEX_DIR = "storage"
_index_cache = {}


def get_index_paths(doc_id: str):
    index_path = os.path.join(INDEX_DIR, f"{doc_id}.index")
    chunks_path = os.path.join(INDEX_DIR, f"{doc_id}_indexed_chunks.json")
    return index_path, chunks_path


def load_or_error(doc_id: str):
    if doc_id in _index_cache:
        return _index_cache[doc_id], None
    index_path, chunks_path = get_index_paths(doc_id)
    if not os.path.exists(index_path):
        return None, f"Document '{doc_id}' not found. Please ingest it first using /tools/ingest"
    index, chunks = load_index(index_path, chunks_path)
    _index_cache[doc_id] = (index, chunks)
    return (index, chunks), None


# ─────────────────────────────────────────
# MCP TOOL 1: Ingest a PDF
# ─────────────────────────────────────────
@app.route("/tools/ingest", methods=["POST"])
def tool_ingest():
    data = request.get_json()
    if not data or "pdf_path" not in data:
        return jsonify({"error": "Missing 'pdf_path' in request body"}), 400

    pdf_path = data["pdf_path"]
    chunk_size = data.get("chunk_size", 400)
    overlap = data.get("overlap", 80)

    if not os.path.exists(pdf_path):
        return jsonify({"error": f"File not found: {pdf_path}"}), 404

    try:
        pages = load_pdf(pdf_path)
        chunks = split_into_chunks(pages, chunk_size=chunk_size, overlap=overlap)

        doc_id = os.path.splitext(os.path.basename(pdf_path))[0]
        doc_id = doc_id.replace(" ", "_")

        chunks_raw_path = os.path.join(INDEX_DIR, f"{doc_id}_chunks.json")
        save_chunks(chunks, chunks_raw_path)

        index_path, chunks_indexed_path = get_index_paths(doc_id)
        index, chunks = build_index(chunks, index_path, chunks_indexed_path)
        _index_cache[doc_id] = (index, chunks)

        return jsonify({
            "status": "success",
            "doc_id": doc_id,
            "pages_loaded": len(pages),
            "chunks_created": len(chunks),
            "index_path": index_path,
            "message": f"Document ingested. Use doc_id='{doc_id}' in all other tools."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────
# MCP TOOL 2: Semantic Search
# ─────────────────────────────────────────
@app.route("/tools/search", methods=["POST"])
def tool_search():
    data = request.get_json()
    if not data or "doc_id" not in data or "query" not in data:
        return jsonify({"error": "Missing 'doc_id' or 'query'"}), 400

    doc_id = data["doc_id"]
    query = data["query"]
    top_k = data.get("top_k", 5)

    cached, err = load_or_error(doc_id)
    if err:
        return jsonify({"error": err}), 404

    index, chunks = cached
    results = search(query, index, chunks, top_k=top_k)

    return jsonify({
        "status": "success",
        "doc_id": doc_id,
        "query": query,
        "results": results
    })


# ─────────────────────────────────────────
# MCP TOOL 3: Extract Clauses
# ─────────────────────────────────────────
@app.route("/tools/extract_clauses", methods=["POST"])
def tool_extract_clauses():
    data = request.get_json()
    if not data or "doc_id" not in data:
        return jsonify({"error": "Missing 'doc_id'"}), 400

    doc_id = data["doc_id"]

    cached, err = load_or_error(doc_id)
    if err:
        return jsonify({"error": err}), 404

    index, chunks = cached
    clauses = extract_clauses(chunks)

    return jsonify({
        "status": "success",
        "doc_id": doc_id,
        "clauses": clauses
    })


# ─────────────────────────────────────────
# MCP TOOL 4: Detect Risks
# ─────────────────────────────────────────
@app.route("/tools/detect_risks", methods=["POST"])
def tool_detect_risks():
    data = request.get_json()
    if not data or "doc_id" not in data:
        return jsonify({"error": "Missing 'doc_id'"}), 400

    doc_id = data["doc_id"]

    cached, err = load_or_error(doc_id)
    if err:
        return jsonify({"error": err}), 404

    index, chunks = cached
    risks = detect_risks(chunks)

    return jsonify({
        "status": "success",
        "doc_id": doc_id,
        "total_risks_found": len(risks),
        "risks": risks
    })


# ─────────────────────────────────────────
# MCP TOOL 5: Full Analysis (all in one)
# ─────────────────────────────────────────
@app.route("/tools/full_analysis", methods=["POST"])
def tool_full_analysis():
    data = request.get_json()
    if not data or "doc_id" not in data:
        return jsonify({"error": "Missing 'doc_id'"}), 400

    doc_id = data["doc_id"]

    cached, err = load_or_error(doc_id)
    if err:
        return jsonify({"error": err}), 404

    index, chunks = cached
    clauses = extract_clauses(chunks)
    risks = detect_risks(chunks)

    high_risks = [r for r in risks if r["severity"] == "HIGH"]
    medium_risks = [r for r in risks if r["severity"] == "MEDIUM"]
    low_risks = [r for r in risks if r["severity"] == "LOW"]

    return jsonify({
        "status": "success",
        "doc_id": doc_id,
        "summary": {
            "total_chunks_analyzed": len(chunks),
            "clauses_found": {k: v["found"] for k, v in clauses.items()},
            "risk_summary": {
                "total": len(risks),
                "high": len(high_risks),
                "medium": len(medium_risks),
                "low": len(low_risks)
            }
        },
        "clauses": clauses,
        "risks": risks
    })


# ─────────────────────────────────────────
# MCP RESOURCE: List available documents
# ─────────────────────────────────────────
@app.route("/resources/documents", methods=["GET"])
def resource_documents():
    files = os.listdir(INDEX_DIR) if os.path.exists(INDEX_DIR) else []
    doc_ids = list(set([
        f.replace(".index", "")
        for f in files
        if f.endswith(".index")
    ]))
    return jsonify({
        "status": "success",
        "documents": doc_ids,
        "count": len(doc_ids)
    })


# ─────────────────────────────────────────
# MCP PROMPT: Describe what this server does
# ─────────────────────────────────────────
@app.route("/prompts/describe", methods=["GET"])
def prompt_describe():
    return jsonify({
        "name": "ClauseLens MCP Server",
        "description": "Contract analysis server. Ingests PDFs, extracts clauses, detects risks.",
        "tools": [
            {
                "name": "ingest",
                "endpoint": "POST /tools/ingest",
                "input": {"pdf_path": "string", "chunk_size": "int (optional)", "overlap": "int (optional)"},
                "output": "doc_id to use in all other tools"
            },
            {
                "name": "search",
                "endpoint": "POST /tools/search",
                "input": {"doc_id": "string", "query": "string", "top_k": "int (optional)"},
                "output": "top matching chunks with scores"
            },
            {
                "name": "extract_clauses",
                "endpoint": "POST /tools/extract_clauses",
                "input": {"doc_id": "string"},
                "output": "termination, payment, renewal, liability clauses with evidence"
            },
            {
                "name": "detect_risks",
                "endpoint": "POST /tools/detect_risks",
                "input": {"doc_id": "string"},
                "output": "list of risks with severity, evidence, confidence"
            },
            {
                "name": "full_analysis",
                "endpoint": "POST /tools/full_analysis",
                "input": {"doc_id": "string"},
                "output": "complete analysis: clauses + risks + summary"
            }
        ]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "server": "ClauseLens MCP Server"})


if __name__ == "__main__":
    os.makedirs(INDEX_DIR, exist_ok=True)
    print("\n========================================")
    print("  ClauseLens MCP Server")
    print("  Running at: http://localhost:5000")
    print("  Health:     http://localhost:5000/health")
    print("========================================\n")
    app.run(host="0.0.0.0", port=5000, debug=False)