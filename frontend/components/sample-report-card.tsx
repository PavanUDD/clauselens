const SAMPLE_FLAGS = [
  { severity: "high", label: "Automatic Renewal Clause" },
  { severity: "medium", label: "Uncapped Liability Exposure" },
] as const;

const SEVERITY_DOT: Record<(typeof SAMPLE_FLAGS)[number]["severity"], string> = {
  high: "bg-risk-high",
  medium: "bg-risk-medium",
};

export function SampleReportCard() {
  return (
    <div className="glass mx-auto w-full max-w-md rounded-2xl p-5 text-left shadow-card sm:p-6">
      <div className="mb-4 flex items-center justify-between gap-2">
        <div className="flex min-w-0 items-center gap-2">
          <span className="h-2.5 w-2.5 shrink-0 rounded-full bg-red-400/70" />
          <span className="h-2.5 w-2.5 shrink-0 rounded-full bg-amber-400/70" />
          <span className="h-2.5 w-2.5 shrink-0 rounded-full bg-emerald-400/70" />
          <span className="ml-1 truncate text-xs text-slate-500">vendor-agreement.pdf</span>
        </div>
        <span className="shrink-0 rounded-full border border-white/10 bg-white/5 px-2.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-slate-400">
          Sample
        </span>
      </div>

      <div className="flex items-center gap-4">
        <div className="relative flex h-16 w-16 shrink-0 items-center justify-center">
          <span aria-hidden className="absolute inset-0 rounded-full bg-amber-500/30 blur-xl" />
          <span className="relative text-4xl font-extrabold text-amber-400">B</span>
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex gap-4 text-sm">
            <span>
              <span className="font-bold text-risk-high">2</span>{" "}
              <span className="text-slate-400">critical</span>
            </span>
            <span>
              <span className="font-bold text-risk-medium">3</span>{" "}
              <span className="text-slate-400">important</span>
            </span>
          </div>
          <p className="mt-1 truncate text-xs text-slate-500">
            Vendor Services Agreement &middot; 7 pages
          </p>
        </div>
      </div>

      <div className="mt-4 space-y-2 border-t border-white/10 pt-4">
        {SAMPLE_FLAGS.map((flag) => (
          <div key={flag.label} className="flex items-center gap-2 text-sm">
            <span className={`h-2 w-2 shrink-0 rounded-full ${SEVERITY_DOT[flag.severity]}`} />
            <span className="truncate text-slate-300">{flag.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
