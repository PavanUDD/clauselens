"""PDF report exporter — generates a branded analysis PDF using reportlab.
Zero external API calls. Generated locally in-memory.
"""
from __future__ import annotations
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

from clauselens.utils.logger import get_logger

log = get_logger(__name__)

# Brand palette (matches Streamlit UI)
BRAND_BLUE = colors.HexColor("#3b82f6")
BRAND_PURPLE = colors.HexColor("#8b5cf6")
TEXT_DARK = colors.HexColor("#111827")
TEXT_MUTED = colors.HexColor("#6b7280")
BG_SOFT = colors.HexColor("#f3f4f6")

SEV_COLORS = {
    "HIGH": colors.HexColor("#ef4444"),
    "MEDIUM": colors.HexColor("#eab308"),
    "LOW": colors.HexColor("#22c55e"),
}

GRADE_COLORS = {
    "A": colors.HexColor("#22c55e"),
    "B": colors.HexColor("#84cc16"),
    "C": colors.HexColor("#eab308"),
    "D": colors.HexColor("#f97316"),
    "F": colors.HexColor("#ef4444"),
}


def _build_styles():
    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=ss["Title"], fontName="Helvetica-Bold",
            fontSize=28, textColor=BRAND_BLUE, spaceAfter=4, alignment=TA_LEFT,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=ss["Normal"], fontName="Helvetica",
            fontSize=11, textColor=TEXT_MUTED, spaceAfter=20,
        ),
        "h2": ParagraphStyle(
            "H2", parent=ss["Heading2"], fontName="Helvetica-Bold",
            fontSize=16, textColor=TEXT_DARK, spaceBefore=16, spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "H3", parent=ss["Heading3"], fontName="Helvetica-Bold",
            fontSize=13, textColor=TEXT_DARK, spaceBefore=10, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body", parent=ss["Normal"], fontName="Helvetica",
            fontSize=10, textColor=TEXT_DARK, leading=14, spaceAfter=6,
        ),
        "muted": ParagraphStyle(
            "Muted", parent=ss["Normal"], fontName="Helvetica",
            fontSize=9, textColor=TEXT_MUTED, leading=12,
        ),
        "quote": ParagraphStyle(
            "Quote", parent=ss["Normal"], fontName="Helvetica-Oblique",
            fontSize=9, textColor=TEXT_DARK, leading=13,
            leftIndent=12, rightIndent=12, spaceAfter=4,
        ),
        "nego": ParagraphStyle(
            "Nego", parent=ss["Normal"], fontName="Helvetica",
            fontSize=9.5, textColor=TEXT_DARK, leading=13,
            leftIndent=12, rightIndent=12, backColor=BG_SOFT,
            borderPadding=8, spaceAfter=6,
        ),
        "center_big": ParagraphStyle(
            "CenterBig", parent=ss["Normal"], fontName="Helvetica-Bold",
            fontSize=48, alignment=TA_CENTER, leading=52,
        ),
        "center_small": ParagraphStyle(
            "CenterSmall", parent=ss["Normal"], fontName="Helvetica",
            fontSize=11, alignment=TA_CENTER, textColor=TEXT_MUTED,
        ),
    }


def _escape(text: str) -> str:
    """Escape HTML-like chars for reportlab Paragraphs."""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def _truncate(text: str, n: int = 500) -> str:
    text = str(text).strip()
    return text if len(text) <= n else text[:n] + "..."


def build_pdf(analysis: dict) -> bytes:
    """Generate the report as PDF bytes. analysis dict comes from main pipeline."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=LETTER,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        title=f"ClauseLens Report — {analysis.get('filename', 'Contract')}",
    )
    styles = _build_styles()
    story = []

    # ---------- HEADER ----------
    story.append(Paragraph("📑 ClauseLens", styles["title"]))
    story.append(Paragraph(
        f"Contract Risk Report · Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        styles["subtitle"],
    ))

    # Contract meta
    meta_data = [
        ["Document", _escape(analysis.get("filename", "—"))],
        ["Contract Type", _escape(str(analysis.get("contract_type", "unknown")).title())],
        ["Classification Confidence", f"{analysis.get('confidence', 0)*100:.0f}%"],
        ["Pages Analyzed", str(analysis.get("pages", 0))],
        ["Chunks Indexed", str(analysis.get("chunks", 0))],
    ]
    meta_table = Table(meta_data, colWidths=[1.8 * inch, 4.7 * inch])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (0, -1), TEXT_MUTED),
        ("TEXTCOLOR", (1, 0), (1, -1), TEXT_DARK),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.HexColor("#e5e7eb")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 18))

    # ---------- HEALTH SCORE ----------
    health = analysis.get("health", {})
    grade = health.get("grade", "—")
    grade_color = GRADE_COLORS.get(grade, TEXT_DARK)

    score_style = ParagraphStyle(
        "ScoreVal", fontName="Helvetica-Bold", fontSize=56,
        textColor=grade_color, alignment=TA_CENTER, leading=60,
    )
    story.append(Paragraph("Contract Health Score", styles["h2"]))
    story.append(Paragraph(
        f"<b>{health.get('score', 0)}</b><font size=20 color='#9ca3af'>/100</font>",
        score_style,
    ))
    story.append(Paragraph(
        f"Grade <b>{grade}</b> — {_escape(health.get('label', ''))}",
        styles["center_small"],
    ))
    story.append(Spacer(1, 14))

    # KPI row
    kpi_data = [[
        f"🔴 {health.get('high_flags', 0)}",
        f"🟡 {health.get('medium_flags', 0)}",
        f"🟢 {health.get('low_flags', 0)}",
    ], ["High Risk", "Medium Risk", "Low Risk"]]
    kpi_table = Table(kpi_data, colWidths=[2.15 * inch] * 3)
    kpi_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 22),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, 1), 9),
        ("TEXTCOLOR", (0, 1), (-1, 1), TEXT_MUTED),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 18))

    # ---------- SUMMARY ----------
    story.append(Paragraph("Plain-English Summary", styles["h2"]))
    summary = analysis.get("summary", "")
    # Convert markdown bold to HTML bold for reportlab
    summary_html = _escape(summary).replace("**", "")  # strip markdown bold asterisks
    for para in summary_html.split("\n\n"):
        para = para.strip()
        if para:
            story.append(Paragraph(para, styles["body"]))
    story.append(Spacer(1, 10))

    # ---------- RISK FLAGS ----------
    flags = analysis.get("flags", [])
    story.append(PageBreak())
    story.append(Paragraph(f"Detailed Risk Flags ({len(flags)})", styles["h2"]))

    if not flags:
        story.append(Paragraph(
            "No risks detected against the rulebook for this contract type.",
            styles["muted"],
        ))
    else:
        for i, flag in enumerate(flags, 1):
            sev = flag.get("severity", "LOW")
            sev_color = SEV_COLORS.get(sev, TEXT_MUTED)
            name = _escape(flag.get("name", ""))
            plain = _escape(flag.get("plain_english", ""))
            typical = _escape(flag.get("typical_range", ""))
            nego = _escape(flag.get("negotiation_script", ""))
            strength = flag.get("match_strength", 0)

            # Header row
            sev_badge_style = ParagraphStyle(
                f"Sev{i}", fontName="Helvetica-Bold", fontSize=9,
                textColor=colors.white, alignment=TA_CENTER, leading=11,
            )
            badge_tbl = Table(
                [[Paragraph(f" {sev} ", sev_badge_style)]],
                colWidths=[0.7 * inch],
            )
            badge_tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), sev_color),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))

            block = [
                badge_tbl,
                Paragraph(f"<b>{i}. {name}</b>", styles["h3"]),
                Paragraph(plain, styles["body"]),
                Paragraph(
                    f"<b>Typical:</b> {typical} &nbsp;&nbsp; "
                    f"<b>Match Strength:</b> {strength}",
                    styles["muted"],
                ),
                Spacer(1, 4),
            ]

            # Evidence
            evidence = flag.get("evidence", [])
            if evidence:
                block.append(Paragraph("<b>Evidence from contract:</b>", styles["muted"]))
                for ev in evidence[:2]:  # limit to 2 per flag in PDF
                    ev_text = _escape(_truncate(ev.get("text", ""), 380))
                    page_num = ev.get("page_num", "?")
                    block.append(Paragraph(f'"{ev_text}"', styles["quote"]))
                    block.append(Paragraph(
                        f"— Page {page_num}",
                        styles["muted"],
                    ))
                    block.append(Spacer(1, 3))

            # Negotiation script
            if nego:
                block.append(Spacer(1, 4))
                block.append(Paragraph("<b>💬 Suggested Negotiation:</b>", styles["muted"]))
                block.append(Paragraph(nego, styles["nego"]))

            block.append(Spacer(1, 14))
            story.append(KeepTogether(block))

    # ---------- FOOTER / DISCLAIMER ----------
    story.append(PageBreak())
    story.append(Paragraph("Privacy & Disclaimer", styles["h2"]))
    story.append(Paragraph(
        "<b>🔒 100% Local · Zero API Calls · Nothing Stored.</b> This report was "
        "generated entirely on your device. Your contract was not sent to any cloud "
        "service or API. No copy of the document or this report is retained by "
        "ClauseLens.",
        styles["body"],
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Not legal advice.</b> ClauseLens is an automated, rule-based analysis "
        "tool. Its output is generated by pattern matching against a curated knowledge "
        "base of contract red flags and industry benchmarks. It is designed as a "
        "first-pass heads-up system — not a substitute for review by a licensed "
        "attorney. Do not rely on ClauseLens alone for decisions with legal or "
        "financial consequences. Always consult a qualified attorney for matters "
        "involving contracts, liability, or your legal rights.",
        styles["body"],
    ))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        f"Report generated by ClauseLens · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["muted"],
    ))

    doc.build(story)
    buf.seek(0)
    pdf_bytes = buf.getvalue()
    log.info(f"PDF report built: {len(pdf_bytes)} bytes")
    return pdf_bytes