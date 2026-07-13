import {
  Briefcase,
  DollarSign,
  Gavel,
  Lightbulb,
  ScrollText,
  ShieldAlert,
  type LucideIcon,
} from "lucide-react";
import type { Flag } from "@/lib/types";
import { RISK_BUCKETS, computeCategoryLevels, type BucketLevel } from "@/lib/categories";

const BUCKET_ICONS: Record<string, LucideIcon> = {
  financial: DollarSign,
  liability: Gavel,
  termination: ScrollText,
  ip: Lightbulb,
  employment: Briefcase,
  compliance: ShieldAlert,
};

const LEVEL_STYLES: Record<
  BucketLevel,
  { badge: string; label: string; iconBg: string }
> = {
  HIGH: {
    badge: "border-risk-high/30 bg-risk-high/15 text-risk-high",
    label: "High",
    iconBg: "bg-risk-high/15",
  },
  MEDIUM: {
    badge: "border-risk-medium/30 bg-risk-medium/15 text-risk-medium",
    label: "Medium",
    iconBg: "bg-risk-medium/15",
  },
  LOW: {
    badge: "border-risk-low/30 bg-risk-low/15 text-risk-low",
    label: "Low",
    iconBg: "bg-risk-low/15",
  },
  CLEAR: {
    badge: "border-risk-low/30 bg-risk-low/15 text-risk-low",
    label: "Clear",
    iconBg: "bg-risk-low/15",
  },
};

export function CategoryBreakdown({ flags }: { flags: Flag[] }) {
  const levels = computeCategoryLevels(flags);

  return (
    <div className="glass animate-fade-in-up rounded-2xl p-6 shadow-card [animation-delay:100ms]">
      <h2 className="text-lg font-semibold text-white">
        Risk Category Breakdown
      </h2>
      <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {RISK_BUCKETS.map(({ key, label }) => {
          const Icon = BUCKET_ICONS[key];
          const level = levels[key];
          const style = LEVEL_STYLES[level];
          return (
            <div
              key={key}
              className="flex flex-col gap-3 rounded-xl border border-white/10 bg-white/2 p-4 transition-all duration-200 hover:-translate-y-0.5 hover:border-white/20 hover:bg-white/4"
            >
              <div className="flex items-center justify-between">
                <span className={`flex h-9 w-9 items-center justify-center rounded-lg ${style.iconBg}`}>
                  <Icon className="h-4.5 w-4.5 text-slate-200" />
                </span>
                <span className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${style.badge}`}>
                  {style.label}
                </span>
              </div>
              <span className="font-medium text-white">{label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
