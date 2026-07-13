"use client";

import { Button } from "@/components/ui/button";
import { GradeSection } from "@/components/analyze/grade-section";
import { CategoryBreakdown } from "@/components/analyze/category-breakdown";
import { DetectedIssues } from "@/components/analyze/detected-issues";
import type { AnalyzeResult } from "@/lib/types";

export function ResultsView({
  result,
  onReset,
}: {
  result: AnalyzeResult;
  onReset: () => void;
}) {
  return (
    <div className="space-y-6">
      <GradeSection health={result.health} />
      <CategoryBreakdown flags={result.flags} />
      <DetectedIssues flags={result.flags} health={result.health} />

      <div className="flex flex-col gap-3 pt-2 sm:flex-row sm:justify-center">
        <Button
          onClick={onReset}
          className="rounded-xl bg-brand-blue text-white shadow-glow-blue transition-all duration-200 hover:bg-brand-blue/90"
        >
          Analyze Another Contract
        </Button>
        <Button
          onClick={() => alert("PDF report export coming soon")}
          className="rounded-xl bg-white/10 text-white transition-all duration-200 hover:bg-white/20"
        >
          Download Report
        </Button>
      </div>
    </div>
  );
}
