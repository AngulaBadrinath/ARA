from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from pathlib import Path
from fastapi import UploadFile, File
import shutil

from app.crud import create_user, get_users, get_user_by_id
from app.schemas import UserCreate, UserResponse
from app.database import check_connection, get_db
from app.models import User

from app.schemas import (
    OrganizationCreate,
    OrganizationResponse,
)

from app.crud import (
    create_organization,
    get_organizations,
)

from app.schemas import ResumeCreate, ResumeResponse

from app.crud import (
    create_resume,
    get_resumes,
    get_resume_by_id,
)

load_dotenv()
import os

print("MAIN DATABASE_URL =", os.getenv("DATABASE_URL"))
print("MAIN POSTGRES_USER =", os.getenv("POSTGRES_USER"))

app = FastAPI(title="ARA Backend", version="0.1.0")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str | bool]:
    db_ok = check_connection()
    return {"status": "ready" if db_ok else "degraded", "database": db_ok}


@app.get("/users/count")
def user_count(db: Session = Depends(get_db)) -> dict[str, int]:
    return {"count": db.query(User).count()}


@app.post("/organizations")
def create_org(
    payload: OrganizationCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_organization(
            db,
            name=payload.name,
            slug=payload.slug,
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Organization slug already exists",
        )


@app.get(
    "/organizations",
    response_model=list[OrganizationResponse],
)
def list_orgs(
    db: Session = Depends(get_db),
):
    return get_organizations(db)


@app.post("/users", response_model=UserResponse)
def create_user_endpoint(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(
        db,
        organization_id=payload.organization_id,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )


@app.get("/users", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
):
    return get_users(db)

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user

@app.post(
    "/resumes",
    response_model=ResumeResponse,
)
def create_resume_endpoint(
    payload: ResumeCreate,
    db: Session = Depends(get_db),
):
    return create_resume(
        db,
        user_id=payload.user_id,
        file_name=payload.file_name,
        file_path=payload.file_path,
        resume_text=payload.resume_text,
    )

@app.get(
    "/resumes/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: UUID,
    db: Session = Depends(get_db),
):
    resume = get_resume_by_id(
        db,
        resume_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    return resume


@app.get(
    "/resumes",
    response_model=list[ResumeResponse],
)
def list_resumes(
    db: Session = Depends(get_db),
):
    return get_resumes(db)      


@app.post("/upload")
def upload_resume(
    file: UploadFile = File(...)
):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return {
        "filename": file.filename,
        "path": str(file_path),
    }
