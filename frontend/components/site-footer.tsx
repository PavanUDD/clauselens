export function SiteFooter() {
  return (
    <footer className="border-t border-white/5 bg-brand-navy">
      <div className="mx-auto max-w-6xl px-6 py-8">
        <p className="text-xs leading-relaxed text-slate-500">
          ClauseLens is an automated risk detection tool, not a law firm.
          This is not legal advice. Always consult a licensed attorney
          before signing contracts with significant legal or financial
          consequences.
        </p>
        <p className="mt-4 text-xs text-slate-500">
          &copy; {new Date().getFullYear()} ClauseLens. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
