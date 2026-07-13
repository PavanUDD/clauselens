import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="glass sticky top-0 z-50 border-x-0 border-t-0">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2.5 transition-transform duration-200 hover:scale-[1.02]">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-linear-to-br from-brand-blue to-brand-cyan text-sm font-bold text-white shadow-glow-blue">
            CL
          </span>
          <span className="text-lg font-semibold tracking-tight text-white">
            ClauseLens
          </span>
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium text-slate-300">
          <Link href="/pricing" className="transition-colors duration-200 hover:text-white">
            Pricing
          </Link>
          <Link
            href="/analyze"
            className="rounded-lg bg-brand-blue px-4 py-2 text-white shadow-glow-blue transition-all duration-200 hover:bg-brand-blue/90 hover:shadow-[0_0_60px_-8px_rgba(37,99,235,0.75)]"
          >
            Analyze a Contract
          </Link>
        </nav>
      </div>
    </header>
  );
}
