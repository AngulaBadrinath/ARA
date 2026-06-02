import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import AnalysisRepository
from app.schemas import AnalysisJobCreate, AnalysisJobDetailResponse, AnalysisJobResponse

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/jobs", response_model=AnalysisJobResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
def create_analysis_job(
    _payload: AnalysisJobCreate,
    _db: Session = Depends(get_db),
) -> AnalysisJobResponse:
    """Enqueue async resume analysis."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


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
