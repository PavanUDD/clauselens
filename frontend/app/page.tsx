import Link from "next/link";
import {
  Briefcase,
  Building2,
  FileLock2,
  FileText,
  Home,
  Scale,
  ShieldCheck,
  Store,
  UserCheck,
  Users,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { SampleReportCard } from "@/components/sample-report-card";

const STATS = [
  { value: "30s", label: "Average Analysis Time" },
  { value: "90+", label: "Rules Checked" },
  { value: "100%", label: "Private Processing" },
];

const USE_CASES = [
  { icon: Building2, label: "IT Staffing Firms" },
  { icon: UserCheck, label: "Independent Consultants" },
  { icon: Store, label: "Small Business Owners" },
  { icon: Scale, label: "Legal Teams" },
];

const CONTRACT_TYPES = [
  {
    icon: FileText,
    label: "Vendor and MSA Agreements",
    description: "Payment terms, liability caps, IP ownership, and termination traps.",
  },
  {
    icon: Users,
    label: "Staffing Agreements",
    description: "Conversion fees, exclusivity clauses, and one-sided termination rights.",
  },
  {
    icon: Briefcase,
    label: "Employment Offers",
    description: "Non-competes, severance gaps, at-will language, and IP assignment.",
  },
  {
    icon: FileLock2,
    label: "NDAs",
    description: "Overbroad definitions, one-way obligations, and indefinite terms.",
  },
  {
    icon: Home,
    label: "Rental Leases",
    description: "Deposit limits, rent increases, subletting rules, and hidden fees.",
  },
];

export default function LandingPage() {
  return (
    <div>
      <section className="relative flex min-h-[92vh] flex-col items-center justify-center overflow-hidden px-4 pb-16 pt-24 text-center sm:px-6 sm:pb-20 sm:pt-28">
        <div
          aria-hidden
          className="pointer-events-none absolute left-1/2 top-[8%] h-105 w-180 -translate-x-1/2 animate-glow-pulse rounded-full bg-brand-blue/30 blur-[110px]"
        />
        <div
          aria-hidden
          className="pointer-events-none absolute left-1/2 top-[18%] h-65 w-120 -translate-x-1/2 rounded-full bg-brand-cyan/20 blur-[100px]"
        />

        <div className="relative mx-auto max-w-4xl animate-fade-in-up">
          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl md:text-7xl">
            Every contract
            <br />
            <span className="bg-linear-to-r from-brand-blue to-brand-cyan bg-clip-text text-transparent">
              has a trap.
            </span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-base text-slate-400 sm:text-lg">
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
          <div className="mx-auto mt-8 flex max-w-xl items-center justify-center gap-2 px-4 text-sm text-slate-500">
            <ShieldCheck className="h-4 w-4 shrink-0 text-brand-cyan" />
            Contract text is processed on our servers during analysis and is
            never stored in our database or shared with third parties.
          </div>

          <div className="relative mt-12 animate-fade-in-up px-4 [animation-delay:100ms] sm:px-0">
            <SampleReportCard />
          </div>
        </div>

        <div className="relative mx-auto mt-16 grid w-full max-w-3xl animate-fade-in-up grid-cols-3 gap-4 [animation-delay:200ms] sm:mt-20 sm:gap-8">
          {STATS.map((stat) => (
            <div key={stat.label} className="text-center">
              <p className="bg-linear-to-b from-brand-cyan to-brand-cyan/70 bg-clip-text text-3xl font-extrabold text-transparent sm:text-5xl">
                {stat.value}
              </p>
              <p className="mt-2 text-xs text-slate-400 sm:text-sm">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-24 sm:px-6 sm:pb-28">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">Built for</h2>
          <p className="mx-auto mt-3 max-w-xl text-slate-400">
            Anyone who signs contracts without a legal team standing behind them.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 sm:gap-6">
          {USE_CASES.map(({ icon: Icon, label }) => (
            <div
              key={label}
              className="glass flex flex-col items-center gap-3 rounded-2xl p-6 text-center shadow-card transition-all duration-200 hover:-translate-y-1"
            >
              <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-blue/15">
                <Icon className="h-6 w-6 text-brand-cyan" />
              </span>
              <span className="text-sm font-medium text-white">{label}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-24 sm:px-6 sm:pb-28">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">What we analyze</h2>
          <p className="mx-auto mt-3 max-w-xl text-slate-400">
            Purpose-built rulebooks for the contracts small businesses sign most.
          </p>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:gap-6 lg:grid-cols-3">
          {CONTRACT_TYPES.map(({ icon: Icon, label, description }) => (
            <div
              key={label}
              className="glass flex flex-col gap-3 rounded-2xl p-6 shadow-card transition-all duration-200 hover:-translate-y-1"
            >
              <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-blue/15">
                <Icon className="h-6 w-6 text-brand-cyan" />
              </span>
              <span className="text-base font-semibold text-white">{label}</span>
              <p className="text-sm leading-relaxed text-slate-400">{description}</p>
            </div>
          ))}
        </div>
        <p className="mx-auto mt-10 max-w-xl text-center text-sm text-slate-500">
          Don&apos;t see your contract type? Upload it anyway — we will do our
          best and flag anything unusual.
        </p>
      </section>
    </div>
  );
}
