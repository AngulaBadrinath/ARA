import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Auth ────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None
    organization_name: str = Field(min_length=1, max_length=255)


class UserResponse(ORMModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None
    organization_id: uuid.UUID
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Resume ──────────────────────────────────────────────────


class ResumeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class ResumeResponse(ORMModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    uploaded_by_id: uuid.UUID
    title: str
    original_filename: str
    content_type: str
    file_size_bytes: int
    created_at: datetime


class PresignedUploadResponse(BaseModel):
    upload_url: str
    storage_key: str
    expires_in_seconds: int


# ── Analysis ────────────────────────────────────────────────


class AnalysisJobCreate(BaseModel):
    resume_id: uuid.UUID


class AnalysisJobResponse(ORMModel):
    id: uuid.UUID
    resume_id: uuid.UUID
    organization_id: uuid.UUID
    status: str
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class AnalysisResultResponse(ORMModel):
    id: uuid.UUID
    job_id: uuid.UUID
    summary: str | None
    skills: list | None
    gaps: list | None
    score: float | None
    suggestions: list | None
    created_at: datetime


class AnalysisJobDetailResponse(AnalysisJobResponse):
    result: AnalysisResultResponse | None = None
