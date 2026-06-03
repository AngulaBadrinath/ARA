import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AnalysisJob, AnalysisJobStatus
from app.repositories import AnalysisRepository, ResumeRepository
from app.schemas import AnalysisJobDetailResponse
from app.services.analysis_service import analyze_pdf

router = APIRouter(prefix="/analysis", tags=["analysis"])

class AnalyzeRequest(BaseModel):
    resume_id: str


@router.post("/jobs")
def create_analysis_job(
    payload: AnalyzeRequest,
    db: Session = Depends(get_db),
):
    resume_repo = ResumeRepository(db)
    analysis_repo = AnalysisRepository(db)

    resume = resume_repo.get_resume(payload.resume_id)

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    job = analysis_repo.create_job(
        resume_id=resume.id,
        organization_id=resume.organization_id,
    )

    result = analyze_pdf(resume.storage_key)

    analysis_repo.create_analysis_result(
        job_id=job.id,
        summary=result.get("summary"),
        skills=result.get("skills", []),
        missing_skills=result.get("missing_skills", []),
        ats_score=result.get("ats_score", 0),
        raw_response=result,
    )

    analysis_repo.update_job_status(
        job.id,
        AnalysisJobStatus.COMPLETED,
    )

    return {
        "job_id": str(job.id),
        "status": "completed",
    }


@router.get("/jobs/{job_id}")
def get_analysis_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    job = (
        db.query(AnalysisJob)
        .filter(AnalysisJob.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "job_id": str(job.id),
        "status": job.status.value,
        "result": {
            "summary": job.result.summary,
            "skills": job.result.skills,
            "gaps": job.result.gaps,
            "score": job.result.score,
        } if job.result else None,
    }