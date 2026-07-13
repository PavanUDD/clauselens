import type { Flag, HealthScore } from "@/lib/types";
import { FlagCard } from "@/components/analyze/flag-card";

const SEVERITY_RANK: Record<Flag["severity"], number> = { HIGH: 3, MEDIUM: 2, LOW: 1 };

export function DetectedIssues({
  flags,
  health,
}: {
  flags: Flag[];
  health: HealthScore;
}) {
  const sortedFlags = [...flags].sort(
    (a, b) => SEVERITY_RANK[b.severity] - SEVERITY_RANK[a.severity]
  );

  return (
    <div className="glass animate-fade-in-up rounded-2xl p-6 shadow-card [animation-delay:200ms]">
      <h2 className="text-lg font-semibold text-white">Detected Issues</h2>

      <div className="mt-4 flex flex-wrap gap-3">
        <span className="rounded-full border border-risk-high/30 bg-risk-high/15 px-3 py-1 text-sm font-semibold text-risk-high">
          {health.high_flags} Critical
        </span>
        <span className="rounded-full border border-risk-medium/30 bg-risk-medium/15 px-3 py-1 text-sm font-semibold text-risk-medium">
          {health.medium_flags} Important
        </span>
        <span className="rounded-full border border-risk-low/30 bg-risk-low/15 px-3 py-1 text-sm font-semibold text-risk-low">
          {health.low_flags} Minor
        </span>
      </div>

      {sortedFlags.length > 0 ? (
        <div className="mt-6 space-y-4">
          {sortedFlags.map((flag) => (
            <FlagCard key={flag.rule_id} flag={flag} />
          ))}
        </div>
      ) : (
        <p className="mt-6 text-sm text-slate-400">
          No risk flags were detected in this contract.
        </p>
      )}
    </div>
  );
}
