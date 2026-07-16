"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { LogOut } from "lucide-react";
import { useAuth } from "@/components/auth-provider";

export function SiteHeader() {
  const { user, loading, signOut } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };

  return (
    <header className="glass sticky top-0 z-50 border-x-0 border-t-0">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-2 px-4 py-4 sm:px-6">
        <Link
          href="/"
          className="flex shrink-0 items-center gap-2.5 transition-transform duration-200 hover:scale-[1.02]"
        >
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-linear-to-br from-brand-blue to-brand-cyan text-sm font-bold text-white shadow-glow-blue">
            CL
          </span>
          <span className="text-lg font-semibold tracking-tight text-white">
            ClauseLens
          </span>
        </Link>
        <nav className="flex items-center gap-2 text-sm font-medium text-slate-300 sm:gap-4">
          <Link
            href="/pricing"
            className="hidden transition-colors duration-200 hover:text-white sm:inline"
          >
            Pricing
          </Link>
          {!loading &&
            (user ? (
              <>
                <Link
                  href="/dashboard"
                  className="max-w-27.5 truncate text-xs text-slate-300 transition-colors duration-200 hover:text-white sm:max-w-45 sm:text-sm"
                >
                  {user.email}
                </Link>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="flex shrink-0 items-center gap-1 rounded-lg border border-white/15 px-2.5 py-1.5 text-xs text-slate-300 transition-colors duration-200 hover:bg-white/5 hover:text-white sm:px-3 sm:text-sm"
                >
                  <LogOut className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </>
            ) : (
              <Link
                href="/login"
                className="shrink-0 rounded-lg border border-white/15 px-2.5 py-1.5 text-xs transition-colors duration-200 hover:bg-white/5 hover:text-white sm:px-3 sm:text-sm"
              >
                Login
              </Link>
            ))}
          <Link
            href="/analyze"
            className="shrink-0 rounded-lg bg-brand-blue px-3 py-1.5 text-xs text-white shadow-glow-blue transition-all duration-200 hover:bg-brand-blue/90 hover:shadow-[0_0_60px_-8px_rgba(37,99,235,0.75)] sm:px-4 sm:py-2 sm:text-sm"
          >
            <span className="sm:hidden">Analyze</span>
            <span className="hidden sm:inline">Analyze a Contract</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
