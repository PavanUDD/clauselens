import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "flex h-10 w-full rounded-lg border border-white/15 bg-white/5 px-3.5 py-2 text-sm text-white placeholder:text-slate-500 transition-colors outline-none focus-visible:border-brand-cyan focus-visible:ring-3 focus-visible:ring-brand-cyan/30 disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
}

export { Input }
