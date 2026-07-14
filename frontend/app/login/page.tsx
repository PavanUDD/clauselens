"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { isSupabaseConfigured, supabase } from "@/lib/supabase";

type Mode = "login" | "signup";

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setMessage(null);

    if (!isSupabaseConfigured) {
      setError(
        "Sign-in isn't configured yet. Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY."
      );
      return;
    }

    setLoading(true);
    try {
      if (mode === "login") {
        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (signInError) throw signInError;
        router.push("/dashboard");
        router.refresh();
      } else {
        const { data, error: signUpError } = await supabase.auth.signUp({
          email,
          password,
        });
        if (signUpError) throw signUpError;
        if (data.session) {
          router.push("/dashboard");
          router.refresh();
        } else {
          setMessage("Check your email to confirm your account, then log in.");
          setMode("login");
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto flex min-h-[80vh] max-w-md flex-col justify-center px-4 py-16 sm:px-6">
      <div className="glass animate-fade-in-up rounded-2xl p-6 shadow-card sm:p-8">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-white">
            {mode === "login" ? "Welcome back" : "Create your account"}
          </h1>
          <p className="mt-2 text-sm text-slate-400">
            {mode === "login"
              ? "Log in to view your saved contract analyses."
              : "Sign up to save and track your contract analyses."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="mb-1.5 block text-sm font-medium text-slate-300">
              Email
            </label>
            <Input
              id="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label htmlFor="password" className="mb-1.5 block text-sm font-medium text-slate-300">
              Password
            </label>
            <Input
              id="password"
              type="password"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
              required
              minLength={6}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="••••••••"
            />
          </div>

          {error && (
            <div className="flex items-start gap-2 rounded-lg border border-risk-high/30 bg-risk-high/10 px-3 py-2 text-sm text-risk-high">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
          {message && (
            <div className="flex items-start gap-2 rounded-lg border border-risk-low/30 bg-risk-low/10 px-3 py-2 text-sm text-risk-low">
              <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" />
              <span>{message}</span>
            </div>
          )}

          <Button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-brand-blue text-white shadow-glow-blue transition-all duration-200 hover:bg-brand-blue/90"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : mode === "login" ? "Log In" : "Sign Up"}
          </Button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          {mode === "login" ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            type="button"
            onClick={() => {
              setMode(mode === "login" ? "signup" : "login");
              setError(null);
              setMessage(null);
            }}
            className="font-medium text-brand-cyan transition-colors hover:text-white"
          >
            {mode === "login" ? "Sign up" : "Log in"}
          </button>
        </p>
      </div>
    </div>
  );
}
