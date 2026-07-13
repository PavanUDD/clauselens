export interface PricingTier {
  name: string;
  price: string;
  period: string;
  description: string;
  features: string[];
  highlighted?: boolean;
  cta: string;
}

export const PRICING_TIERS: PricingTier[] = [
  {
    name: "Starter",
    price: "Free",
    period: "",
    description: "Try ClauseLens on a single contract.",
    features: [
      "1 contract analysis per month",
      "Full risk category breakdown",
      "Plain-English clause explanations",
      "Contract Review Grade",
    ],
    cta: "Get Started",
  },
  {
    name: "Pro",
    price: "$49",
    period: "/month",
    description: "For individuals who review contracts regularly.",
    features: [
      "Unlimited contract analyses",
      "Full risk category breakdown",
      "Negotiation scripts for every flag",
      "Priority processing",
      "Email support",
    ],
    highlighted: true,
    cta: "Start Free Trial",
  },
  {
    name: "Business",
    price: "$149",
    period: "/month",
    description: "For teams reviewing contracts at scale.",
    features: [
      "Everything in Pro",
      "Multi-seat team access",
      "Shared contract history",
      "Custom rulebooks",
      "Priority support",
    ],
    cta: "Contact Sales",
  },
];
