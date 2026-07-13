import type { Flag, Severity } from "@/lib/types";

export type RiskBucket =
  | "financial"
  | "liability"
  | "termination"
  | "ip"
  | "employment"
  | "compliance";

export const RISK_BUCKETS: { key: RiskBucket; label: string }[] = [
  { key: "financial", label: "Financial Risk" },
  { key: "liability", label: "Liability Risk" },
  { key: "termination", label: "Termination Risk" },
  { key: "ip", label: "IP Risk" },
  { key: "employment", label: "Employment Risk" },
  { key: "compliance", label: "Compliance Risk" },
];

// Maps the raw `flag.category` strings produced by the rule engine
// (see clauselens/rulebook/*.py) to the six buckets shown on the results page.
const CATEGORY_TO_BUCKET: Record<string, RiskBucket> = {
  payment: "financial",
  collateral: "financial",
  deposit: "financial",
  default: "financial",
  legal: "liability",
  termination: "termination",
  renewal: "termination",
  ip: "ip",
  restriction: "employment",
  benefits: "employment",
  scope: "employment",
  compliance: "compliance",
  confidentiality: "compliance",
  privacy: "compliance",
  data: "compliance",
  service: "compliance",
  maintenance: "compliance",
  obligations: "compliance",
  terms: "compliance",
  unknown: "compliance",
};

export function bucketForCategory(category: string): RiskBucket {
  return CATEGORY_TO_BUCKET[category] ?? "compliance";
}

export type BucketLevel = "HIGH" | "MEDIUM" | "LOW" | "CLEAR";

const SEVERITY_RANK: Record<Severity, number> = { HIGH: 3, MEDIUM: 2, LOW: 1 };

export function computeCategoryLevels(flags: Flag[]): Record<RiskBucket, BucketLevel> {
  const result = {} as Record<RiskBucket, BucketLevel>;

  for (const { key } of RISK_BUCKETS) {
    const flagsInBucket = flags.filter((f) => bucketForCategory(f.category) === key);
    if (flagsInBucket.length === 0) {
      result[key] = "CLEAR";
      continue;
    }
    const worst = flagsInBucket.reduce(
      (max, f) => Math.max(max, SEVERITY_RANK[f.severity]),
      0
    );
    result[key] = worst === 3 ? "HIGH" : worst === 2 ? "MEDIUM" : "LOW";
  }

  return result;
}

export const GRADE_ACTION: Record<
  string,
  { label: string; colorClass: string }
> = {
  A: { label: "Looks Standard", colorClass: "text-risk-low" },
  B: { label: "Review Recommended", colorClass: "text-risk-medium" },
  C: { label: "Significant Concerns", colorClass: "text-risk-medium" },
  D: { label: "Legal Review Recommended", colorClass: "text-risk-high" },
  F: { label: "Do Not Sign Without Attorney", colorClass: "text-risk-high" },
};
