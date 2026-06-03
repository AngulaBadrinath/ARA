from uuid import UUID
from pydantic import BaseModel, EmailStr


class OrganizationCreate(BaseModel):
    name: str
    slug: str


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    organization_id: UUID
    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    id: UUID
    organization_id: UUID
    email: EmailStr
    full_name: str | None
    is_active: bool

    class Config:
        from_attributes = True

class ResumeCreate(BaseModel):
    user_id: UUID
    file_name: str
    file_path: str
    resume_text: str | None = None
    

class ResumeResponse(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    file_path: str
    status: str

    class Config:
        from_attributes = True 