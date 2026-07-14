import { GRADE_ACTION, RISK_BUCKETS, computeCategoryLevels, type BucketLevel } from "@/lib/categories";
import type { AnalyzeResult, Flag, Severity } from "@/lib/types";

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

const GRADE_COLORS: Record<AnalyzeResult["health"]["grade"], string> = {
  A: "#059669",
  B: "#059669",
  C: "#D97706",
  D: "#DC2626",
  F: "#DC2626",
};

const LEVEL_COLORS: Record<BucketLevel, { text: string; bg: string }> = {
  HIGH: { text: "#DC2626", bg: "#FEE2E2" },
  MEDIUM: { text: "#D97706", bg: "#FEF3C7" },
  LOW: { text: "#059669", bg: "#D1FAE5" },
  CLEAR: { text: "#059669", bg: "#D1FAE5" },
};

const SEVERITY_LABEL: Record<Severity, string> = {
  HIGH: "Critical",
  MEDIUM: "Important",
  LOW: "Minor",
};

const SEVERITY_COLORS: Record<Severity, string> = {
  HIGH: "#DC2626",
  MEDIUM: "#D97706",
  LOW: "#059669",
};

function formatDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function renderFlag(flag: Flag): string {
  const color = SEVERITY_COLORS[flag.severity];
  return `
    <div style="border-left:4px solid ${color}; background:#F8FAFC; border-radius:8px; padding:16px 20px; margin-bottom:14px; page-break-inside:avoid;">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
        <span style="display:inline-block; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.03em; color:${color}; background:${color}1A; border:1px solid ${color}55; border-radius:999px; padding:2px 10px;">
          ${escapeHtml(SEVERITY_LABEL[flag.severity])}
        </span>
        <span style="font-size:15px; font-weight:700; color:#0F172A;">${escapeHtml(flag.name)}</span>
      </div>
      <p style="margin:0 0 8px; font-size:13px; color:#334155; line-height:1.5;">${escapeHtml(flag.plain_english)}</p>
      <p style="margin:0 0 8px; font-size:12px; color:#64748B; line-height:1.5;">${escapeHtml(flag.explanation)}</p>
      ${
        flag.negotiation_script
          ? `<div style="margin-top:8px; padding:10px 12px; background:#EEF2FF; border-radius:6px;">
              <p style="margin:0 0 2px; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.03em; color:#4338CA;">Suggested Negotiation Language</p>
              <p style="margin:0; font-size:12px; font-style:italic; color:#312E81;">&ldquo;${escapeHtml(flag.negotiation_script)}&rdquo;</p>
            </div>`
          : ""
      }
      ${
        flag.typical_range
          ? `<p style="margin:8px 0 0; font-size:11px; color:#64748B;"><strong>Typical range:</strong> ${escapeHtml(flag.typical_range)}</p>`
          : ""
      }
    </div>
  `;
}

export function buildReportHtml(result: AnalyzeResult): string {
  const levels = computeCategoryLevels(result.flags);
  const gradeColor = GRADE_COLORS[result.health.grade] ?? "#334155";
  const action = GRADE_ACTION[result.health.grade];
  const sortedFlags = [...result.flags].sort((a, b) => {
    const rank: Record<Severity, number> = { HIGH: 3, MEDIUM: 2, LOW: 1 };
    return rank[b.severity] - rank[a.severity];
  });

  const categoryCards = RISK_BUCKETS.map(({ key, label }) => {
    const level = levels[key];
    const colors = LEVEL_COLORS[level];
    return `
      <div style="border:1px solid #E2E8F0; border-radius:8px; padding:12px 14px; display:flex; align-items:center; justify-content:space-between;">
        <span style="font-size:13px; font-weight:600; color:#0F172A;">${escapeHtml(label)}</span>
        <span style="font-size:11px; font-weight:700; color:${colors.text}; background:${colors.bg}; border-radius:999px; padding:2px 10px;">
          ${level === "CLEAR" ? "Clear" : level.charAt(0) + level.slice(1).toLowerCase()}
        </span>
      </div>
    `;
  }).join("");

  const flagsHtml =
    sortedFlags.length > 0
      ? sortedFlags.map(renderFlag).join("")
      : `<p style="font-size:13px; color:#64748B;">No risk flags were detected in this contract.</p>`;

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>ClauseLens Report — ${escapeHtml(result.filename)}</title>
<style>
  @media print {
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .page-break { page-break-before: always; }
  }
  @media screen and (max-width: 600px) {
    body { padding: 20px; }
    .category-grid { grid-template-columns: 1fr !important; }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 48px;
    background: #FFFFFF;
    color: #0F172A;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }
  .container { max-width: 720px; margin: 0 auto; }
  .report-header, .grade-row { flex-wrap: wrap; }
</style>
</head>
<body>
  <div class="container">
    <div class="report-header" style="display:flex; align-items:center; justify-content:space-between; border-bottom:2px solid #0F172A; padding-bottom:16px; margin-bottom:24px; gap:12px;">
      <div style="display:flex; align-items:center; gap:10px;">
        <span style="display:flex; height:32px; width:32px; align-items:center; justify-content:center; border-radius:8px; background:#2563EB; color:#fff; font-weight:700; font-size:13px;">CL</span>
        <span style="font-size:18px; font-weight:700; color:#0F172A;">ClauseLens</span>
      </div>
      <div style="text-align:right;">
        <p style="margin:0; font-size:12px; color:#64748B;">Contract Risk Report</p>
        <p style="margin:0; font-size:12px; color:#64748B;">${escapeHtml(formatDate(result.analyzed_at))}</p>
      </div>
    </div>

    <div class="grade-row" style="display:flex; align-items:center; gap:28px; margin-bottom:28px;">
      <div style="flex-shrink:0; width:88px; height:88px; border-radius:50%; border:4px solid ${gradeColor}; display:flex; align-items:center; justify-content:center;">
        <span style="font-size:40px; font-weight:800; color:${gradeColor};">${escapeHtml(result.health.grade)}</span>
      </div>
      <div style="min-width:200px;">
        <p style="margin:0 0 4px; font-size:20px; font-weight:700; color:#0F172A;">${escapeHtml(result.contract_type)}</p>
        <p style="margin:0 0 6px; font-size:14px; font-weight:600; color:${gradeColor};">${escapeHtml(action?.label ?? result.health.label)}</p>
        <p style="margin:0; font-size:12px; color:#64748B;">${escapeHtml(result.filename)} &middot; ${result.page_count} pages &middot; ${result.health.total_flags} flags detected</p>
      </div>
    </div>

    <h2 style="font-size:14px; text-transform:uppercase; letter-spacing:0.04em; color:#334155; margin:0 0 12px;">Risk Category Breakdown</h2>
    <div class="category-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:28px;">
      ${categoryCards}
    </div>

    <h2 style="font-size:14px; text-transform:uppercase; letter-spacing:0.04em; color:#334155; margin:0 0 12px;">Detected Issues</h2>
    <div style="margin-bottom:24px;">
      ${flagsHtml}
    </div>

    <div style="border-top:1px solid #E2E8F0; padding-top:16px; margin-top:32px;">
      <p style="font-size:10px; line-height:1.6; color:#94A3B8; margin:0;">
        ClauseLens is an automated risk detection tool, not a law firm. This report reflects
        detected risk patterns based on automated rule matching and is not legal advice or a
        determination that this contract is safe to sign. Always consult a licensed attorney
        before signing contracts with significant legal or financial consequences.
      </p>
      <p style="font-size:10px; color:#CBD5E1; margin:8px 0 0;">&copy; ${new Date().getFullYear()} ClauseLens. All rights reserved.</p>
    </div>
  </div>
</body>
</html>`;
}

export function openReportWindow(result: AnalyzeResult): boolean {
  const reportWindow = window.open("", "_blank", "width=900,height=1200");
  if (!reportWindow) return false;

  reportWindow.document.open();
  reportWindow.document.write(buildReportHtml(result));
  reportWindow.document.close();
  reportWindow.focus();

  setTimeout(() => {
    reportWindow.print();
  }, 300);

  return true;
}
