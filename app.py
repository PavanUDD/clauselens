"""ClauseLens — Streamlit UI entry point.

Run with:  streamlit run app.py
"""
from __future__ import annotations
import tempfile
from pathlib import Path

import streamlit as st

from clauselens.ingestion.pdf_loader import load_pdf
from clauselens.ingestion.chunker import split_into_chunks
from clauselens.classification.contract_classifier import classify
from clauselens.retrieval.search import build_index
from clauselens.analysis.term_extractor import extract_all_terms
from clauselens.analysis.risk_engine import evaluate
from clauselens.analysis.health_score import compute as compute_health
from clauselens.analysis.summarizer import summarize
from clauselens.ui.styles import inject as inject_css
from clauselens.ui.components import (
    render_health_score, render_kpi_row, render_meta_row,
    render_risk_flag, render_summary, render_privacy_footer,
    render_empty_state,
)
from config import APP_NAME, APP_TAGLINE


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title=f"{APP_NAME} — {APP_TAGLINE}",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <h1 style="font-size:1.8rem;margin-bottom:0;">📑 {APP_NAME}</h1>
        <p style="color:#a1a1aa;font-size:0.85rem;margin:0.25rem 0 0 0;">{APP_TAGLINE}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📤 Upload Contract")
    uploaded_file = st.file_uploader(
        "Drop a PDF here",
        type=["pdf"],
        label_visibility="collapsed",
        key="uploader",
    )

    st.markdown("---")

    if st.button("🗑️ Clear All Data", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("""
    <div style="margin-top:2rem;padding:1rem;background:#0f0f17;border:1px solid #1f1f2e;border-radius:10px;font-size:0.8rem;color:#a1a1aa;line-height:1.6;">
        <strong style="color:#60a5fa;">🔒 Privacy-First</strong><br>
        Your contract is processed entirely in-memory. Nothing is saved to disk.
        No API calls. No telemetry. Close the tab and it's gone.
    </div>
    """, unsafe_allow_html=True)


# ---------- MAIN ----------
st.markdown(f"# {APP_NAME}")
st.markdown(f'<p style="color:#a1a1aa;font-size:1.1rem;margin-top:-0.5rem;">{APP_TAGLINE}</p>',
            unsafe_allow_html=True)


def run_analysis(pdf_bytes: bytes, filename: str) -> dict:
    """Run full pipeline on uploaded PDF bytes. Returns analysis dict."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
        tf.write(pdf_bytes)
        tmp_path = Path(tf.name)
    try:
        pages = load_pdf(tmp_path)
        chunks = split_into_chunks(pages)
        contract_type, confidence, scores = classify(chunks)
        index, chunks = build_index(chunks)
        terms = extract_all_terms(chunks)
        flags = evaluate(chunks, contract_type, terms)
        health = compute_health(flags)
        summary = summarize(contract_type, terms, flags, health)
        return {
            "filename": filename,
            "contract_type": contract_type,
            "confidence": confidence,
            "pages": len(pages),
            "chunks": len(chunks),
            "terms": terms,
            "flags": [f.to_dict() for f in flags],
            "health": health,
            "summary": summary,
        }
    finally:
        try:
            tmp_path.unlink()
        except Exception:
            pass


# ---------- FLOW ----------
if uploaded_file is None and "analysis" not in st.session_state:
    render_empty_state()
    render_privacy_footer()
    st.stop()

# New file uploaded → run analysis
if uploaded_file is not None:
    file_key = f"{uploaded_file.name}-{uploaded_file.size}"
    if st.session_state.get("file_key") != file_key:
        with st.spinner("🔍 Analyzing your contract... (first run takes ~30s to load the model)"):
            st.session_state.analysis = run_analysis(uploaded_file.read(), uploaded_file.name)
            st.session_state.file_key = file_key

analysis = st.session_state.get("analysis")
if not analysis:
    render_empty_state()
    render_privacy_footer()
    st.stop()


# ---------- RENDER REPORT ----------
st.markdown(f"### 📄 {analysis['filename']}")
render_meta_row(
    analysis["contract_type"],
    analysis["confidence"],
    analysis["pages"],
    analysis["chunks"],
)

col1, col2 = st.columns([1, 1])
with col1:
    render_health_score(analysis["health"])
with col2:
    render_kpi_row(analysis["health"])

tab1, tab2, tab3 = st.tabs(["📊 Summary", "🚨 Risk Flags", "📑 Contract Details"])

with tab1:
    st.markdown("## Plain-English Summary")
    render_summary(analysis["summary"])

with tab2:
    st.markdown(f"## {len(analysis['flags'])} Risk Flags Detected")
    if not analysis["flags"]:
        st.info("No risks detected against the rulebook for this contract type.")
    else:
        for i, flag in enumerate(analysis["flags"], 1):
            render_risk_flag(flag, i)

with tab3:
    st.markdown("## Document Intelligence")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Monetary Amounts Found", analysis["terms"]["money_count"])
    with col_b:
        st.metric("Percentages Found", analysis["terms"]["percentage_count"])
    with col_c:
        st.metric("Durations Found", analysis["terms"]["duration_count"])

    if analysis["terms"]["money_amounts"]:
        st.markdown("**💰 Monetary values extracted:**")
        st.code(", ".join(f"${m:,.0f}" for m in analysis["terms"]["money_amounts"][:20]))
    if analysis["terms"]["durations"]:
        st.markdown("**⏱️ Durations referenced:**")
        st.code(", ".join(analysis["terms"]["durations"][:20]))

render_privacy_footer()