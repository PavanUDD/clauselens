"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { AlertCircle } from "lucide-react";
import { Dropzone } from "@/components/analyze/dropzone";
import { ProcessingState } from "@/components/analyze/processing-state";
import { ResultsView } from "@/components/analyze/results-view";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/components/auth-provider";
import { analyzeContract, getJobResults } from "@/lib/api";
import { isSupabaseConfigured, supabase } from "@/lib/supabase";
import type { AnalyzeResult } from "@/lib/types";

type Stage = "upload" | "processing" | "results" | "error";

const POLL_INTERVAL_MS = 2000;

async function saveAnalysis(userId: string, result: AnalyzeResult) {
  if (!isSupabaseConfigured) return;
  try {
    await supabase.from("analyses").insert({
      user_id: userId,
      filename: result.filename,
      contract_type: result.contract_type,
      grade: result.health.grade,
      high_flags: result.health.high_flags,
      medium_flags: result.health.medium_flags,
      low_flags: result.health.low_flags,
      analyzed_at: result.analyzed_at,
    });
  } catch {
    // Saving analysis history is best-effort and should never block the results view.
  }
}

export default function AnalyzePage() {
  const { user } = useAuth();
  const [stage, setStage] = useState<Stage>("upload");
  const [filename, setFilename] = useState<string>();
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const pollTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const userIdRef = useRef<string | null>(null);

  useEffect(() => {
    userIdRef.current = user?.id ?? null;
  }, [user]);

  useEffect(() => {
    return () => {
      if (pollTimer.current) clearTimeout(pollTimer.current);
    };
  }, []);

  const pollForResults = useCallback((jobId: string) => {
    const tick = async () => {
      try {
        const status = await getJobResults(jobId);
        if (status.status === "complete") {
          setResult(status);
          setStage("results");
          if (userIdRef.current) {
            void saveAnalysis(userIdRef.current, status);
          }
          return;
        }
        pollTimer.current = setTimeout(tick, POLL_INTERVAL_MS);
      } catch (err) {
        setErrorMessage(
          err instanceof Error ? err.message : "Something went wrong while analyzing your contract."
        );
        setStage("error");
      }
    };
    pollTimer.current = setTimeout(tick, POLL_INTERVAL_MS);
  }, []);

  const handleFileSelected = useCallback(
    async (file: File) => {
      setFilename(file.name);
      setErrorMessage(null);
      setStage("processing");
      try {
        const accepted = await analyzeContract(file);
        pollForResults(accepted.job_id);
      } catch (err) {
        setErrorMessage(
          err instanceof Error ? err.message : "Failed to upload contract."
        );
        setStage("error");
      }
    },
    [pollForResults]
  );

  const handleReset = useCallback(() => {
    if (pollTimer.current) clearTimeout(pollTimer.current);
    setStage("upload");
    setResult(null);
    setErrorMessage(null);
    setFilename(undefined);
  }, []);

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 sm:py-16">
      {stage === "upload" && (
        <div className="animate-fade-in-up">
          <div className="mb-8 text-center">
            <h1 className="text-3xl font-bold text-white sm:text-4xl">
              Analyze Your Contract
            </h1>
            <p className="mt-2 text-slate-400">
              Upload a PDF and we&apos;ll flag the risky clauses in seconds.
            </p>
          </div>
          <Dropzone onFileSelected={handleFileSelected} />
        </div>
      )}

      {stage === "processing" && (
        <div className="animate-fade-in-up">
          <ProcessingState filename={filename} />
        </div>
      )}

      {stage === "error" && (
        <div className="glass animate-fade-in-up flex flex-col items-center gap-4 rounded-2xl border-risk-high/30 px-6 py-16 text-center shadow-glow-red">
          <AlertCircle className="h-10 w-10 text-risk-high" />
          <p className="text-lg font-medium text-white">Analysis failed</p>
          <p className="max-w-md text-sm text-slate-300">{errorMessage}</p>
          <Button
            onClick={handleReset}
            className="mt-2 rounded-xl bg-brand-blue text-white shadow-glow-blue transition-all duration-200 hover:bg-brand-blue/90"
          >
            Try Again
          </Button>
        </div>
      )}

      {stage === "results" && result && (
        <ResultsView result={result} onReset={handleReset} />
      )}
    </div>
  );
}
