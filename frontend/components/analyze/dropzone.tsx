"use client";

import { useCallback, useRef, useState } from "react";
import { FileText, UploadCloud } from "lucide-react";
import { cn } from "@/lib/utils";

interface DropzoneProps {
  onFileSelected: (file: File) => void;
  disabled?: boolean;
  error?: string | null;
}

export function Dropzone({ onFileSelected, disabled, error }: DropzoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndSelect = useCallback(
    (file: File | undefined) => {
      if (!file) return;
      const isPdf =
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf");
      if (!isPdf) {
        setLocalError("Only PDF files are supported. Please upload a .pdf file.");
        return;
      }
      setLocalError(null);
      onFileSelected(file);
    },
    [onFileSelected]
  );

  const handleDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragging(false);
      if (disabled) return;
      validateAndSelect(event.dataTransfer.files?.[0]);
    },
    [disabled, validateAndSelect]
  );

  const displayError = error ?? localError;

  return (
    <div className="w-full">
      <div
        role="button"
        tabIndex={0}
        onClick={() => !disabled && inputRef.current?.click()}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            inputRef.current?.click();
          }
        }}
        onDragOver={(event) => {
          event.preventDefault();
          if (!disabled) setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        aria-disabled={disabled}
        className={cn(
          "group glass flex flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed px-4 py-14 text-center shadow-card transition-all duration-200 sm:px-6 sm:py-20",
          isDragging
            ? "border-brand-cyan bg-brand-cyan/5 shadow-glow-cyan"
            : "border-white/15 hover:border-brand-cyan/50 hover:shadow-glow-blue",
          disabled && "pointer-events-none opacity-60"
        )}
      >
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-brand-blue/20 transition-transform duration-200 group-hover:scale-110">
          <UploadCloud className="h-8 w-8 text-brand-cyan" />
        </div>
        <div>
          <p className="text-lg font-medium text-white">
            Drop your contract here, or click to browse
          </p>
          <p className="mt-1 flex items-center justify-center gap-1.5 text-sm text-slate-400">
            <FileText className="h-4 w-4" />
            PDF files only
          </p>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf,.pdf"
          className="hidden"
          disabled={disabled}
          onChange={(event) => validateAndSelect(event.target.files?.[0])}
        />
      </div>
      {displayError && (
        <p className="mt-3 text-center text-sm text-risk-high">{displayError}</p>
      )}
    </div>
  );
}
