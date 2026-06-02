/** Shared API contract types — keep in sync with FastAPI OpenAPI schema. */

export type AnalysisJobStatus = "pending" | "processing" | "completed" | "failed";

export interface UserSummary {
  id: string;
  email: string;
  full_name: string | null;
  organization_id: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface ResumeSummary {
  id: string;
  organization_id: string;
  uploaded_by_id: string;
  title: string;
  original_filename: string;
  content_type: string;
  file_size_bytes: number;
  created_at: string;
}

export interface PresignedUploadResponse {
  upload_url: string;
  storage_key: string;
  expires_in_seconds: number;
}

export interface AnalysisJobSummary {
  id: string;
  resume_id: string;
  organization_id: string;
  status: AnalysisJobStatus;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface AnalysisResultSummary {
  id: string;
  job_id: string;
  summary: string | null;
  skills: string[] | null;
  gaps: string[] | null;
  score: number | null;
  suggestions: string[] | null;
  created_at: string;
}

export interface AnalysisJobDetail extends AnalysisJobSummary {
  result: AnalysisResultSummary | null;
}

export const API_ROUTES = {
  health: "/api/v1/health",
  ready: "/api/v1/ready",
  auth: {
    register: "/api/v1/auth/register",
    login: "/api/v1/auth/login",
  },
  resumes: {
    list: "/api/v1/resumes/",
    uploadUrl: "/api/v1/resumes/upload-url",
  },
  analysis: {
    createJob: "/api/v1/analysis/jobs",
    getJob: (id: string) => `/api/v1/analysis/jobs/${id}`,
  },
} as const;
