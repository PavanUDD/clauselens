import { TriangleAlert } from "lucide-react";

const SUPPORTED_CONTRACT_TYPES = [
  "vendor",
  "staffing",
  "employment",
  "nda",
  "rental",
];

const CONFIDENCE_THRESHOLD = 0.5;

export function isOutOfCoverage(contractType: string, confidence: number) {
  return (
    contractType === "unknown" ||
    confidence < CONFIDENCE_THRESHOLD ||
    !SUPPORTED_CONTRACT_TYPES.includes(contractType)
  );
}

export function CoverageWarning() {
  return (
    <div className="glass animate-fade-in-up flex gap-3 rounded-2xl border border-amber-500/30 p-4 shadow-glow-amber sm:p-5">
      <TriangleAlert className="mt-0.5 h-5 w-5 flex-shrink-0 text-amber-400" aria-hidden />
      <p className="text-sm leading-relaxed text-amber-100">
        <span className="font-semibold text-amber-300">Heads up</span> — this
        contract type may be outside our current coverage. ClauseLens is
        optimized for Vendor/MSA Agreements, Staffing Agreements, Employment
        Offers, NDAs, and Rental Leases. Results below are based on our
        general rules and may miss contract-specific risks. We recommend
        attorney review for this document type.
      </p>
    </div>
  );
}
