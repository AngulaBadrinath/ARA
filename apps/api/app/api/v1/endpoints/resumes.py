import uuid
import shutil

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File 
from pathlib import Path
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import ResumeRepository
from app.schemas import PresignedUploadResponse, ResumeCreate, ResumeResponse

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
async def upload_resume(file: UploadFile = File(...)):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "path": str(file_path)
    }
