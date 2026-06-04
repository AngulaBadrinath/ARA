import uuid
import shutil
import os

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from uuid import UUID 
from pathlib import Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Resume
from app.repositories import ResumeRepository
from app.schemas import PresignedUploadResponse, ResumeCreate, ResumeResponse
from app.services.resume_parser import extract_text_from_pdf

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("/", response_model=list[ResumeResponse], status_code=status.HTTP_501_NOT_IMPLEMENTED)
def list_resumes(
    _organization_id: uuid.UUID,
    _db: Session = Depends(get_db), 
) -> list[ResumeResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
def create_resume(
    _payload: ResumeCreate,
    _db: Session = Depends(get_db),
) -> ResumeResponse:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{resume_id}", response_model=ResumeResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_resume(
    resume_id: uuid.UUID,
    organization_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> ResumeResponse:
    resume = ResumeRepository(db).get_by_id(resume_id, organization_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post(
    "/upload-url",
    response_model=PresignedUploadResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def create_upload_url(_db: Session = Depends(get_db)) -> PresignedUploadResponse:
    """Return presigned URL for direct upload to object storage."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db),):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(file_path)
    
    resume = Resume(
        organization_id=UUID("2a3fa96b-e453-467a-954d-f230703c6349"),
        uploaded_by_id=UUID("b5ec2751-fdcc-42ce-b0a9-2ceeb5674b24"),
        title=file.filename.replace(".pdf", ""),
        original_filename=file.filename,
        storage_key=str(file_path),
        content_type=file.content_type,
        file_size_bytes=os.path.getsize(file_path),
        extracted_text=extracted_text,
    )

    resume_repo = ResumeRepository(db)
    saved_resume = resume_repo.create(resume)

    return {
        "resume_id": str(saved_resume.id),
        "filename": saved_resume.original_filename,
        "characters": len(extracted_text),
    }
