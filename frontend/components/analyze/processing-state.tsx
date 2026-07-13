import { FileSearch } from "lucide-react";

interface ProcessingStateProps {
  filename?: string;
}

export function ProcessingState({ filename }: ProcessingStateProps) {
  return (
    <div className="glass flex flex-col items-center justify-center gap-8 rounded-2xl px-6 py-24 text-center shadow-card">
      <div className="relative flex h-28 w-28 items-center justify-center">
        <span className="absolute inset-0 rounded-full border-2 border-brand-cyan animate-ring-pulse" />
        <span className="absolute inset-0 rounded-full border-2 border-brand-cyan animate-ring-pulse [animation-delay:0.7s]" />
        <span className="absolute inset-0 rounded-full border-2 border-brand-cyan animate-ring-pulse [animation-delay:1.4s]" />
        <div className="relative flex h-16 w-16 items-center justify-center rounded-full bg-linear-to-br from-brand-blue to-brand-cyan shadow-glow-blue">
          <FileSearch className="h-8 w-8 text-white" />
        </div>
      </div>
      <div>
        <p className="text-xl font-medium text-white">
          Analyzing your contract...
        </p>
        {filename && (
          <p className="mt-1 text-sm text-slate-400">{filename}</p>
        )}
        <p className="mt-3 text-sm text-slate-500">
          This usually takes under a minute.
        </p>
      </div>
    </div>
  );
}
