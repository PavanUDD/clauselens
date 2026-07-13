export type Severity = "HIGH" | "MEDIUM" | "LOW";

export interface Flag {
  rule_id: string;
  name: string;
  severity: Severity;
  category: string;
  plain_english: string;
  explanation: string;
  negotiation_script: string;
  typical_range: string | null;
  evidence: unknown[];
  match_strength: number;
  learn_more: string | null;
}

export interface HealthScore {
  score: number;
  grade: "A" | "B" | "C" | "D" | "F";
  label: string;
  high_flags: number;
  medium_flags: number;
  low_flags: number;
  total_flags: number;
}

export interface AnalyzeResult {
  contract_type: string;
  confidence: number;
  page_count: number;
  chunk_count: number;
  health: HealthScore;
  flags: Flag[];
  terms: Record<string, unknown>;
  timings: Record<string, number>;
  filename: string;
  analyzed_at: string;
}

export interface AnalyzeAcceptedResponse {
  job_id: string;
  status: "processing";
  request_id: string;
}

export type JobStatusResponse =
  | { status: "processing"; job_id: string }
  | ({ status: "complete"; job_id: string } & AnalyzeResult);

export interface ApiErrorBody {
  status?: string;
  message?: string;
  job_id?: string;
}
