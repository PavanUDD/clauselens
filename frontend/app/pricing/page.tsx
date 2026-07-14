import type { Metadata } from "next";
import { PricingCards } from "@/components/pricing-cards";

export const metadata: Metadata = {
  title: "Pricing — ClauseLens",
};

export default function PricingPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6 sm:py-20">
      <div className="mb-12 animate-fade-in-up text-center">
        <h1 className="text-4xl font-bold text-white sm:text-5xl">
          Simple, transparent pricing
        </h1>
        <p className="mx-auto mt-3 max-w-xl text-slate-400">
          Every plan includes the full risk detection engine. Upgrade for
          unlimited analyses and team features.
        </p>
      </div>
      <PricingCards />
    </div>
  );
}
