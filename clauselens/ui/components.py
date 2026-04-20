"""Reusable Streamlit UI components for ClauseLens."""
from __future__ import annotations
import html
import streamlit as st


def render_health_score(health: dict) -> None:
    """Big circular health-score display."""
    grade = health["grade"]
    st.markdown(f"""
    <div class="health-score">
        <div class="health-score-value grade-{grade}">{health['score']}<span style="font-size:2rem;color:#71717a;">/100</span></div>
        <div class="health-score-label">Grade {grade} — {health['label']}</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_row(health: dict) -> None:
    """Three KPI cards: HIGH / MEDIUM / LOW flag counts."""
    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-value kpi-high">{health['high_flags']}</div>
            <div class="kpi-label">🔴 High Risk</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value kpi-med">{health['medium_flags']}</div>
            <div class="kpi-label">🟡 Medium Risk</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value kpi-low">{health['low_flags']}</div>
            <div class="kpi-label">🟢 Low Risk</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_meta_row(contract_type: str, confidence: float, pages: int, chunks: int) -> None:
    """Contract meta info strip."""
    st.markdown(f"""
    <div class="meta-row" style="margin-bottom:1.5rem;">
        <span>📄 Type: <strong>{contract_type.title()}</strong></span>
        <span>🎯 Classification: <strong>{confidence*100:.0f}%</strong></span>
        <span>📖 Pages: <strong>{pages}</strong></span>
        <span>🧩 Chunks: <strong>{chunks}</strong></span>
    </div>
    """, unsafe_allow_html=True)


def render_risk_flag(flag: dict, index: int) -> None:
    """A single risk flag card with evidence and negotiation script."""
    sev = flag["severity"]
    name = html.escape(flag["name"])
    plain = html.escape(flag["plain_english"])
    typical = html.escape(flag["typical_range"])
    nego = html.escape(flag["negotiation_script"])

    # Top card
    st.markdown(f"""
    <div class="risk-card severity-{sev}">
        <span class="risk-badge badge-{sev}">{sev}</span>
        <div class="risk-title">{index}. {name}</div>
        <div class="risk-plain">{plain}</div>
        <div class="meta-row">
            <span>✅ Typical: <strong>{typical}</strong></span>
            <span>📊 Match Strength: <strong>{flag['match_strength']}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Evidence expandable
    with st.expander(f"📄 View evidence from contract ({len(flag['evidence'])} chunks matched)", expanded=False):
        for ev in flag["evidence"]:
            evidence_text = html.escape(ev["text"])
            st.markdown(f"""
            <div class="evidence-quote">
                "{evidence_text}"
                <div class="evidence-page">— Page {ev['page_num']}, Chunk {ev['chunk_id']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="nego-block">
            <div class="nego-label">💬 Suggested Negotiation Script</div>
            {nego}
        </div>
        """, unsafe_allow_html=True)


def render_summary(summary_md: str) -> None:
    """Render the plain-English summary as a nice block."""
    st.markdown(f'<div class="summary-block">{summary_md}</div>', unsafe_allow_html=True)


def render_privacy_footer() -> None:
    """Privacy reassurance footer."""
    st.markdown("""
    <div class="privacy-footer">
        🔒 <strong>100% Local · Zero API Calls · Nothing Stored</strong><br>
        Your contract never leaves your browser session. Close the tab and it's gone.
        <br><br>
        <em>ClauseLens is an automated analysis tool — not legal advice. Consult a licensed attorney for any decision with legal or financial consequences.</em>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state() -> None:
    """Shown before any contract is uploaded."""
    st.markdown("""
    <div class="hero-card">
        <h2 style="margin-top:0;">👋 Welcome to ClauseLens</h2>
        <p style="color:#a1a1aa; font-size:1.05rem; line-height:1.7;">
            Upload any contract PDF — rental, employment, freelance, or otherwise — and get an instant risk analysis:
        </p>
        <ul style="color:#d4d4d8; line-height:2;">
            <li>📊 <strong>Contract Health Score</strong> — an at-a-glance 0-100 rating</li>
            <li>🚨 <strong>Red flags</strong> detected against a curated rulebook</li>
            <li>💬 <strong>Negotiation scripts</strong> ready to send to the counterparty</li>
            <li>📝 <strong>Plain-English summary</strong> of what you're signing</li>
            <li>🔒 <strong>100% local</strong> — your document never leaves your browser</li>
        </ul>
        <p style="color:#71717a; margin-top:1rem; font-size:0.9rem;">
            👈 Upload a PDF using the sidebar to begin.
        </p>
    </div>
    """, unsafe_allow_html=True)