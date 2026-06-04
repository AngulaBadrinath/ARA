import type {
  AnalysisJobDetail,
  AnalysisJobSummary,
  ResumeSummary,
  TokenResponse,
  UserSummary,
} from "@ara/shared-types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(
      `Request failed: ${response.statusText}`,
      response.status,
    );
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  health: () => request<{ status: string }>("/api/v1/health"),

  register: (body: unknown) =>
    request<UserSummary>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  login: (body: unknown) =>
    request<TokenResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  listResumes: () => request<ResumeSummary[]>("/api/v1/resumes/"),

  createAnalysisJob: (body: { resume_id: string }) =>
    request<AnalysisJobSummary>("/api/v1/analysis/jobs", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  getAnalysisJob: (jobId: string) =>
    request<AnalysisJobDetail>(`/api/v1/analysis/jobs/${jobId}`),
};

export { ApiError };
