import type { Flag } from "@/lib/types";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const SEVERITY_STYLES: Record<
  Flag["severity"],
  { badge: string; label: string; border: string }
> = {
  HIGH: {
    badge: "bg-risk-high/15 text-risk-high border-risk-high/30",
    label: "Critical",
    border: "border-l-risk-high",
  },
  MEDIUM: {
    badge: "bg-risk-medium/15 text-risk-medium border-risk-medium/30",
    label: "Important",
    border: "border-l-risk-medium",
  },
  LOW: {
    badge: "bg-risk-low/15 text-risk-low border-risk-low/30",
    label: "Minor",
    border: "border-l-risk-low",
  },
};

export function FlagCard({ flag }: { flag: Flag }) {
  const severity = SEVERITY_STYLES[flag.severity];

  return (
    <div
      className={`rounded-xl border border-white/10 border-l-4 bg-white/2 p-5 shadow-card transition-all duration-200 hover:-translate-y-0.5 hover:bg-white/4 ${severity.border}`}
    >
      <div className="flex items-start gap-4">
        <span
          className={`mt-0.5 shrink-0 rounded-full border px-2.5 py-1 text-xs font-semibold ${severity.badge}`}
        >
          {severity.label}
        </span>
        <div className="min-w-0 flex-1">
          <h3 className="font-bold text-white">{flag.name}</h3>
          <p className="mt-1 text-sm text-slate-300">{flag.plain_english}</p>

          <Accordion className="mt-3">
            <AccordionItem className="border-b-0">
              <AccordionTrigger className="text-sm font-medium text-brand-cyan hover:no-underline">
                View Details
              </AccordionTrigger>
              <AccordionContent>
                <div className="space-y-4 border-t border-white/10 pt-4">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Explanation
                    </p>
                    <p className="mt-1 text-sm text-slate-300">
                      {flag.explanation}
                    </p>
                  </div>
                  {flag.negotiation_script && (
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                        Suggested language to start the conversation
                      </p>
                      <p className="mt-1 rounded-lg bg-white/5 p-3 text-sm italic text-slate-300">
                        &ldquo;{flag.negotiation_script}&rdquo;
                      </p>
                    </div>
                  )}
                  {flag.typical_range && (
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                        Typical Range
                      </p>
                      <p className="mt-1 text-sm text-slate-300">
                        {flag.typical_range}
                      </p>
                    </div>
                  )}
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </div>
  );
}
