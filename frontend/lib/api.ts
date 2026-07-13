import type { AnalyzeAcceptedResponse, ApiErrorBody, JobStatusResponse } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function requireApiUrl(): string {
  if (!API_URL) {
    throw new ApiError(
      "NEXT_PUBLIC_API_URL is not configured. Set it in your environment to point at the ClauseLens API.",
      500
    );
  }
  return API_URL;
}

async function extractErrorMessage(response: Response): Promise<string> {
  try {
    const body = await response.json();
    const detail = (body?.detail ?? body) as ApiErrorBody | string | undefined;
    if (typeof detail === "string") return detail;
    if (detail?.message) return detail.message;
  } catch {
    // response body wasn't JSON — fall through to generic message
  }
  return `Request failed with status ${response.status}`;
}

export async function analyzeContract(file: File): Promise<AnalyzeAcceptedResponse> {
  const baseUrl = requireApiUrl();
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${baseUrl}/api/v1/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new ApiError(await extractErrorMessage(response), response.status);
  }

  return response.json();
}

export async function getJobResults(jobId: string): Promise<JobStatusResponse> {
  const baseUrl = requireApiUrl();
  const response = await fetch(`${baseUrl}/api/v1/results/${jobId}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new ApiError(await extractErrorMessage(response), response.status);
  }

  return response.json();
}
