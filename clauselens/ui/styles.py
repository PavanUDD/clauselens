"""Premium dark-theme CSS for ClauseLens Streamlit UI."""

CUSTOM_CSS = """
<style>
/* Import Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global resets */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* App background - near black */
.stApp {
    background: linear-gradient(180deg, #0a0a0f 0%, #0f0f17 100%);
    color: #e4e4e7;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}
[data-testid="stDecoration"] {display: none;}

/* Main block padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0a0f;
    border-right: 1px solid #1f1f2e;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* Typography */
h1 {
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem !important;
}
h2 {
    font-weight: 700 !important;
    color: #f4f4f5 !important;
    letter-spacing: -0.01em !important;
    margin-top: 2rem !important;
}
h3 {
    font-weight: 600 !important;
    color: #d4d4d8 !important;
}

/* Hero card */
.hero-card {
    background: linear-gradient(135deg, rgba(59,130,246,0.08) 0%, rgba(167,139,250,0.08) 100%);
    border: 1px solid #1f1f2e;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

/* Health Score gauge */
.health-score {
    text-align: center;
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid #1f1f2e;
    background: #0f0f17;
}
.health-score-value {
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
}
.health-score-label {
    font-size: 1.1rem;
    color: #a1a1aa;
    margin-top: 0.5rem;
    font-weight: 500;
}
.grade-A {color: #22c55e;}
.grade-B {color: #84cc16;}
.grade-C {color: #eab308;}
.grade-D {color: #f97316;}
.grade-F {color: #ef4444;}

/* KPI cards */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}
.kpi-card {
    background: #0f0f17;
    border: 1px solid #1f1f2e;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    transition: transform 0.15s, border-color 0.15s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: #3b3b52;
}
.kpi-value {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
}
.kpi-label {
    font-size: 0.85rem;
    color: #a1a1aa;
    margin-top: 0.5rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.kpi-high {color: #ef4444;}
.kpi-med {color: #eab308;}
.kpi-low {color: #22c55e;}

/* Risk flag cards */
.risk-card {
    background: #0f0f17;
    border-left: 4px solid #3b82f6;
    border-top: 1px solid #1f1f2e;
    border-right: 1px solid #1f1f2e;
    border-bottom: 1px solid #1f1f2e;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.risk-card.severity-HIGH {border-left-color: #ef4444;}
.risk-card.severity-MEDIUM {border-left-color: #eab308;}
.risk-card.severity-LOW {border-left-color: #22c55e;}

.risk-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-HIGH {background: rgba(239,68,68,0.15); color: #f87171;}
.badge-MEDIUM {background: rgba(234,179,8,0.15); color: #facc15;}
.badge-LOW {background: rgba(34,197,94,0.15); color: #4ade80;}

.risk-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f4f4f5;
    margin: 0.5rem 0 0.25rem 0;
}
.risk-plain {
    color: #a1a1aa;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

/* Evidence quote block */
.evidence-quote {
    background: #060609;
    border-left: 3px solid #3b82f6;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    font-family: 'Georgia', serif;
    font-style: italic;
    color: #d4d4d8;
    font-size: 0.9rem;
    border-radius: 4px;
    line-height: 1.6;
}
.evidence-page {
    font-size: 0.75rem;
    color: #71717a;
    margin-top: 0.25rem;
    font-style: normal;
}

/* Meta info row */
.meta-row {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin-top: 0.75rem;
    font-size: 0.85rem;
    color: #a1a1aa;
}
.meta-row span strong {color: #e4e4e7;}

/* Negotiation script block */
.nego-block {
    background: linear-gradient(135deg, rgba(59,130,246,0.05), rgba(167,139,250,0.05));
    border: 1px solid #1f2937;
    border-radius: 8px;
    padding: 0.9rem 1rem;
    margin-top: 0.75rem;
    font-size: 0.9rem;
    color: #cbd5e1;
}
.nego-label {
    font-size: 0.7rem;
    color: #60a5fa;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.15s;
    box-shadow: 0 2px 8px rgba(59,130,246,0.2);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(59,130,246,0.3);
}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
    background: #0f0f17;
    border: 2px dashed #3b3b52;
    border-radius: 14px;
    padding: 2rem;
    transition: border-color 0.15s;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #60a5fa;
}

/* Privacy footer */
.privacy-footer {
    background: #0a0a0f;
    border-top: 1px solid #1f1f2e;
    padding: 1rem;
    margin-top: 3rem;
    text-align: center;
    font-size: 0.85rem;
    color: #71717a;
}

/* Summary block */
.summary-block {
    background: #0f0f17;
    border: 1px solid #1f1f2e;
    border-radius: 12px;
    padding: 1.5rem;
    line-height: 1.7;
    color: #d4d4d8;
}

/* Expander custom */
.streamlit-expanderHeader {
    background: #0f0f17 !important;
    border-radius: 8px !important;
}

/* Alerts */
[data-testid="stAlert"] {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 10px;
}

/* Tabs */
[data-testid="stTabs"] button[role="tab"] {
    background: transparent;
    color: #a1a1aa;
    font-weight: 500;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #60a5fa;
    border-bottom-color: #3b82f6;
}
</style>
"""


def inject():
    """Inject custom CSS into Streamlit. Call this at the top of app.py."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)