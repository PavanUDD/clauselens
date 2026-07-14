import type { HealthScore } from "@/lib/types";
import { GRADE_ACTION } from "@/lib/categories";

const GRADE_GLOW: Record<HealthScore["grade"], { glow: string; text: string }> = {
  A: { glow: "bg-emerald-500/40 shadow-glow-green", text: "text-emerald-400" },
  B: { glow: "bg-emerald-500/40 shadow-glow-green", text: "text-emerald-400" },
  C: { glow: "bg-amber-500/40 shadow-glow-amber", text: "text-amber-400" },
  D: { glow: "bg-red-500/40 shadow-glow-red", text: "text-red-400" },
  F: { glow: "bg-red-500/40 shadow-glow-red", text: "text-red-400" },
};

export function GradeSection({ health }: { health: HealthScore }) {
  const action = GRADE_ACTION[health.grade] ?? {
    label: health.label,
    colorClass: "text-slate-300",
  };
  const gradeStyle = GRADE_GLOW[health.grade] ?? GRADE_GLOW.C;

  return (
    <div className="glass animate-fade-in-up rounded-2xl p-6 text-center shadow-card sm:p-8">
      <p className="text-sm font-medium uppercase tracking-wide text-slate-400">
        Contract Review Grade
      </p>
      <div className="relative mx-auto mt-4 flex h-32 w-32 items-center justify-center sm:h-40 sm:w-40">
        <span
          aria-hidden
          className={`absolute inset-0 rounded-full blur-3xl ${gradeStyle.glow}`}
        />
        <p className={`relative text-7xl font-extrabold leading-none sm:text-8xl ${gradeStyle.text}`}>
          {health.grade}
        </p>
      </div>
      <p className={`mt-4 text-lg font-semibold ${action.colorClass}`}>
        {action.label}
      </p>
      <p className="mx-auto mt-4 max-w-xl text-xs leading-relaxed text-slate-500">
        This assessment reflects detected risk patterns. It is not legal
        advice or a determination that this contract is safe to sign.
      </p>
    </div>
  );
}
