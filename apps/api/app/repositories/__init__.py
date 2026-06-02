import uuid

from sqlalchemy.orm import Session

from app.models import AnalysisJob, Resume, User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()


class ResumeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, resume_id: uuid.UUID, organization_id: uuid.UUID) -> Resume | None:
        return (
            self.db.query(Resume)
            .filter(Resume.id == resume_id, Resume.organization_id == organization_id)
            .first()
        )

    def list_by_organization(self, organization_id: uuid.UUID) -> list[Resume]:
        return (
            self.db.query(Resume)
            .filter(Resume.organization_id == organization_id)
            .order_by(Resume.created_at.desc())
            .all()
        )


class AnalysisRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_job(self, job_id: uuid.UUID, organization_id: uuid.UUID) -> AnalysisJob | None:
        return (
            self.db.query(AnalysisJob)
            .filter(AnalysisJob.id == job_id, AnalysisJob.organization_id == organization_id)
            .first()
        )
