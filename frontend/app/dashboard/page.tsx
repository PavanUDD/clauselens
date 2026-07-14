"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FileText, Loader2, Upload } from "lucide-react";
import { useAuth } from "@/components/auth-provider";
import { isSupabaseConfigured, supabase } from "@/lib/supabase";
import type { AnalysisRecord } from "@/lib/types";

const GRADE_STYLES: Record<string, string> = {
  A: "text-risk-low border-risk-low/30 bg-risk-low/10",
  B: "text-risk-low border-risk-low/30 bg-risk-low/10",
  C: "text-risk-medium border-risk-medium/30 bg-risk-medium/10",
  D: "text-risk-high border-risk-high/30 bg-risk-high/10",
  F: "text-risk-high border-risk-high/30 bg-risk-high/10",
};

function formatDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export default function DashboardPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [analyses, setAnalyses] = useState<AnalysisRecord[]>([]);
  const [loadingAnalyses, setLoadingAnalyses] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [authLoading, user, router]);

  useEffect(() => {
    if (!user || !isSupabaseConfigured) {
      setLoadingAnalyses(false);
      return;
    }

    let isMounted = true;
    setLoadingAnalyses(true);

    supabase
      .from("analyses")
      .select("id, user_id, filename, contract_type, grade, high_flags, medium_flags, low_flags, analyzed_at")
      .eq("user_id", user.id)
      .order("analyzed_at", { ascending: false })
      .then(({ data, error }) => {
        if (!isMounted) return;
        if (error) {
          setFetchError(error.message);
        } else {
          setAnalyses((data as AnalysisRecord[]) ?? []);
        }
        setLoadingAnalyses(false);
      });

    return () => {
      isMounted = false;
    };
  }, [user]);

  if (authLoading || !user) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-brand-cyan" />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 sm:py-16">
      <div className="glass animate-fade-in-up mb-6 flex flex-col gap-4 rounded-2xl p-6 shadow-card sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <p className="truncate text-lg font-semibold text-white">{user.email}</p>
          <p className="mt-1 text-sm text-slate-400">Manage your account and view analysis history.</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="rounded-full border border-brand-cyan/30 bg-brand-cyan/10 px-3 py-1 text-xs font-semibold text-brand-cyan">
            Free Plan
          </span>
          <Link
            href="/pricing"
            className="rounded-lg bg-brand-blue px-3 py-1.5 text-xs font-medium text-white shadow-glow-blue transition-all duration-200 hover:bg-brand-blue/90"
          >
            Upgrade
          </Link>
        </div>
      </div>

      <div className="glass animate-fade-in-up rounded-2xl p-6 shadow-card [animation-delay:100ms]">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Your Analyses</h2>
          <Link
            href="/analyze"
            className="flex items-center gap-1.5 text-sm font-medium text-brand-cyan transition-colors hover:text-white"
          >
            <Upload className="h-4 w-4" />
            New Analysis
          </Link>
        </div>

        {loadingAnalyses ? (
          <div className="flex justify-center py-12">
            <Loader2 className="h-6 w-6 animate-spin text-brand-cyan" />
          </div>
        ) : fetchError ? (
          <p className="py-8 text-center text-sm text-slate-400">
            Couldn&apos;t load your analysis history right now.
          </p>
        ) : analyses.length === 0 ? (
          <div className="flex flex-col items-center gap-3 py-12 text-center">
            <FileText className="h-8 w-8 text-slate-500" />
            <p className="text-sm text-slate-400">
              No contracts analyzed yet. Upload your first contract.
            </p>
            <Link
              href="/analyze"
              className="mt-2 rounded-xl bg-brand-blue px-5 py-2 text-sm font-medium text-white shadow-glow-blue transition-all duration-200 hover:bg-brand-blue/90"
            >
              Analyze a Contract
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-white/10">
            {analyses.map((analysis) => (
              <div
                key={analysis.id}
                className="flex flex-col gap-2 py-4 sm:flex-row sm:items-center sm:justify-between"
              >
                <div className="min-w-0">
                  <p className="truncate font-medium text-white">{analysis.filename}</p>
                  <p className="mt-0.5 text-sm text-slate-400">
                    {analysis.contract_type} &middot; {formatDate(analysis.analyzed_at)}
                  </p>
                </div>
                <div className="flex shrink-0 items-center gap-3">
                  <span className="text-xs text-slate-400">
                    {analysis.high_flags} critical &middot; {analysis.medium_flags} important
                  </span>
                  <span
                    className={`flex h-8 w-8 items-center justify-center rounded-full border text-sm font-bold ${
                      GRADE_STYLES[analysis.grade] ?? "text-slate-300 border-white/15 bg-white/5"
                    }`}
                  >
                    {analysis.grade}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
