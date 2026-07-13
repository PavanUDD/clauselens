import Link from "next/link";
import { ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PricingCards } from "@/components/pricing-cards";

const STATS = [
  { value: "30s", label: "Average Analysis Time" },
  { value: "90+", label: "Rules Checked" },
  { value: "100%", label: "Private Processing" },
];

export default function LandingPage() {
  return (
    <div>
      <section className="relative flex min-h-[92vh] flex-col items-center justify-center overflow-hidden px-6 pb-20 pt-28 text-center">
        <div
          aria-hidden
          className="pointer-events-none absolute left-1/2 top-[8%] h-[420px] w-[720px] -translate-x-1/2 animate-glow-pulse rounded-full bg-brand-blue/30 blur-[110px]"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute left-1/2 top-[18%] h-[260px] w-[480px] -translate-x-1/2 rounded-full bg-brand-cyan/20 blur-[100px]"
        />

        <div className="relative mx-auto max-w-4xl animate-fade-in-up">
          <h1 className="text-5xl font-bold tracking-tight text-white sm:text-7xl">
            Every contract
            <br />
            <span className="bg-linear-to-r from-brand-blue to-brand-cyan bg-clip-text text-transparent">
              has a trap.
            </span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400">
            Upload any contract and get a plain-English breakdown of the risky
            clauses, hidden obligations, and one-sided terms buried inside —
            in seconds, not billable hours.
          </p>
          <div className="mt-10 flex justify-center">
            <Button
              render={<Link href="/analyze" />}
              nativeButton={false}
              size="lg"
              className="h-14 rounded-2xl bg-brand-blue px-10 text-base font-semibold text-white shadow-glow-blue transition-all duration-200 hover:-translate-y-0.5 hover:bg-brand-blue/90 hover:shadow-[0_0_80px_-8px_rgba(37,99,235,0.8)]"
            >
              Analyze Your Contract
            </Button>
          </div>
          <div className="mx-auto mt-8 flex max-w-xl items-center justify-center gap-2 text-sm text-slate-500">
            <ShieldCheck className="h-4 w-4 shrink-0 text-brand-cyan" />
            Contract text is processed temporarily and never stored in our
            database.
          </div>
        </div>

        <div className="relative mx-auto mt-24 grid w-full max-w-3xl animate-fade-in-up grid-cols-1 gap-8 [animation-delay:150ms] sm:grid-cols-3">
          {STATS.map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="bg-linear-to-b from-brand-cyan to-brand-cyan/70 bg-clip-text text-5xl font-extrabold text-transparent">
                {stat.value}
              </p>
              <p className="mt-2 text-sm text-slate-400">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-28">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">
            Simple, transparent pricing
          </h2>
          <p className="mt-3 text-slate-400">
            Start free. Upgrade when you need more.
          </p>
        </div>
        <PricingCards />
      </section>
    </div>
  );
}
