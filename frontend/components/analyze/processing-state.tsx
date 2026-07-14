import { FileSearch } from "lucide-react";

interface ProcessingStateProps {
  filename?: string;
}

export function ProcessingState({ filename }: ProcessingStateProps) {
  return (
    <div className="glass flex flex-col items-center justify-center gap-8 rounded-2xl px-4 py-16 text-center shadow-card sm:px-6 sm:py-24">
      <div className="relative flex h-28 w-28 shrink-0 items-center justify-center">
        <span className="absolute inset-0 rounded-full border-2 border-brand-cyan animate-ring-pulse" />
        <span className="absolute inset-0 rounded-full border-2 border-brand-cyan animate-ring-pulse [animation-delay:0.7s]" />
        <span className="absolute inset-0 rounded-full border-2 border-brand-cyan animate-ring-pulse [animation-delay:1.4s]" />
        <div className="relative flex h-16 w-16 items-center justify-center rounded-full bg-linear-to-br from-brand-blue to-brand-cyan shadow-glow-blue">
          <FileSearch className="h-8 w-8 text-white" />
        </div>
      </div>
      <div className="w-full max-w-xs">
        <p className="text-xl font-medium text-white">
          Analyzing your contract...
        </p>
        {filename && (
          <p className="mt-1 wrap-break-word text-sm text-slate-400">{filename}</p>
        )}
        <p className="mt-3 text-sm text-slate-500">
          This usually takes under a minute.
        </p>
      </div>
    </div>
  );
}
