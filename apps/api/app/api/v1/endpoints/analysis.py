import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import AnalysisRepository
from app.schemas import AnalysisJobCreate, AnalysisJobDetailResponse, AnalysisJobResponse

from app.services.analysis_service import analyze_pdf

router = APIRouter(prefix="/analysis", tags=["analysis"])
@router.post("/jobs")
def create_analysis_job(
    _payload: AnalysisJobCreate,
    _db: Session = Depends(get_db),
):
    result = analyze_pdf(
        r"C:\Projects\ARA\backend\uploads\AB Resume.pdf"
    )

    return {
        "status": "completed",
        "analysis": result["analysis"],
    }


@router.get(
    "/jobs/{job_id}",
    response_model=AnalysisJobDetailResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def get_analysis_job(
    job_id: uuid.UUID,
    organization_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> AnalysisJobDetailResponse:
    job = AnalysisRepository(db).get_job(job_id, organization_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
