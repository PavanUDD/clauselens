import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        card: "var(--card)",
        "card-foreground": "var(--card-foreground)",
        popover: "var(--popover)",
        "popover-foreground": "var(--popover-foreground)",
        primary: "var(--primary)",
        "primary-foreground": "var(--primary-foreground)",
        secondary: "var(--secondary)",
        "secondary-foreground": "var(--secondary-foreground)",
        muted: "var(--muted)",
        "muted-foreground": "var(--muted-foreground)",
        accent: "var(--accent)",
        "accent-foreground": "var(--accent-foreground)",
        destructive: "var(--destructive)",
        "destructive-foreground": "var(--destructive-foreground)",
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
        brand: {
          navy: "#0A0F1E",
          panel: "#0D1B3E",
          blue: "#2563EB",
          cyan: "#38BDF8",
        },
        risk: {
          high: "#EF4444",
          medium: "#F59E0B",
          low: "#10B981",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      boxShadow: {
        "glow-blue": "0 0 50px -10px rgba(37, 99, 235, 0.55)",
        "glow-cyan": "0 0 50px -10px rgba(56, 189, 248, 0.5)",
        "glow-green": "0 0 60px -8px rgba(16, 185, 129, 0.45)",
        "glow-amber": "0 0 60px -8px rgba(245, 158, 11, 0.45)",
        "glow-red": "0 0 60px -8px rgba(239, 68, 68, 0.45)",
        card: "0 8px 30px -12px rgba(0, 0, 0, 0.6)",
      },
    },
  },
  plugins: [],
};
export default config;
