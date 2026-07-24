import uuid
import shutil
import os

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pathlib import Path
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models import Resume, AnalysisJob
from app.repositories import ResumeRepository
from app.schemas import PresignedUploadResponse, ResumeCreate, ResumeResponse
from app.services.resume_parser import extract_text_from_pdf

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Create uploads directory
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    # Save file
    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    extracted_text = extract_text_from_pdf(str(file_path))

    # Create Resume object
    resume = Resume(
        organization_id=current_user.organization_id,
        uploaded_by_id=current_user.id,
        title=file.filename.replace(".pdf", ""),
        original_filename=file.filename,
        storage_key=str(file_path),
        content_type=file.content_type,
        file_size_bytes=os.path.getsize(file_path),
        extracted_text=extracted_text,
    )

    # Save to database
    resume_repo = ResumeRepository(db)
    saved_resume = resume_repo.create(resume)

    return {
        "resume_id": str(saved_resume.id),
        "filename": saved_resume.original_filename,
        "characters": len(extracted_text),
    }

@router.get("")
def list_resumes(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resumes = ResumeRepository(db).list_by_organization(
        current_user.organization_id
    )

    return [
        {
            "id": str(resume.id),
            "title": resume.title,
            "filename": resume.original_filename,
            "created_at": resume.created_at,
        }
        for resume in resumes
    ]


@router.get("/{resume_id}")
def get_resume(
    resume_id: uuid.UUID,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = ResumeRepository(db).get_by_id(
        resume_id,
        current_user.organization_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    return {
        "id": str(resume.id),
        "title": resume.title,
        "filename": resume.original_filename,
        "content_type": resume.content_type,
        "file_size_bytes": resume.file_size_bytes,
        "created_at": resume.created_at,
    }


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: uuid.UUID,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = ResumeRepository(db).get_by_id(
        resume_id,
        current_user.organization_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    # Delete associated analysis jobs and results first
    jobs = db.query(AnalysisJob).filter(AnalysisJob.resume_id == resume_id).all()
    for job in jobs:
        if job.result:
            db.delete(job.result)
        db.delete(job)

    db.delete(resume)
    db.commit()

    return {"status": "deleted"}


