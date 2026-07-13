import { Check } from "lucide-react";
import Link from "next/link";
import { PRICING_TIERS } from "@/lib/pricing";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function PricingCards() {
  return (
    <div className="grid gap-6 md:grid-cols-3">
      {PRICING_TIERS.map((tier) => (
        <Card
          key={tier.name}
          className={`glass relative flex flex-col overflow-visible rounded-2xl border p-1 shadow-card transition-all duration-200 hover:-translate-y-1 ${
            tier.highlighted
              ? "border-brand-cyan/60 shadow-glow-cyan"
              : "border-white/10"
          }`}
        >
          <CardHeader>
            {tier.highlighted && (
              <span className="absolute -top-3 left-1/2 w-fit -translate-x-1/2 rounded-full bg-linear-to-r from-brand-blue to-brand-cyan px-3 py-1 text-xs font-semibold text-white shadow-glow-cyan">
                Most Popular
              </span>
            )}
            <CardTitle className="text-xl text-white">{tier.name}</CardTitle>
            <div className="flex items-baseline gap-1 pt-2">
              <span className="text-3xl font-bold text-white">
                {tier.price}
              </span>
              {tier.period && (
                <span className="text-sm text-slate-400">{tier.period}</span>
              )}
            </div>
            <p className="pt-2 text-sm text-slate-400">{tier.description}</p>
          </CardHeader>
          <CardContent className="flex flex-1 flex-col gap-6">
            <ul className="flex-1 space-y-3">
              {tier.features.map((feature) => (
                <li
                  key={feature}
                  className="flex items-start gap-2 text-sm text-slate-300"
                >
                  <Check className="mt-0.5 h-4 w-4 shrink-0 text-brand-cyan" />
                  {feature}
                </li>
              ))}
            </ul>
            <Button
              render={<Link href="/analyze" />}
              nativeButton={false}
              className={`w-full rounded-xl transition-all duration-200 ${
                tier.highlighted
                  ? "bg-brand-blue text-white shadow-glow-blue hover:bg-brand-blue/90"
                  : "bg-white/10 text-white hover:bg-white/20"
              }`}
            >
              {tier.cta}
            </Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
