import uuid

from sqlalchemy.orm import Session

from app.models import AnalysisJob, AnalysisJobStatus, AnalysisResult, Resume, User, Organization


class UserRepository:

    def create(
        self,
        user: User,
    ) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()


class ResumeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, resume: Resume) -> Resume:
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def get_by_id(self, resume_id: uuid.UUID, organization_id: uuid.UUID) -> Resume | None:
        return (
            self.db.query(Resume)
            .filter(Resume.id == resume_id, Resume.organization_id == organization_id)
            .first()
        )

    def get_resume(self, resume_id):
        return (
            self.db.query(Resume)
            .filter(Resume.id == resume_id)
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

    def get_job(
        self,
        job_id: uuid.UUID,
        organization_id: uuid.UUID,
    ) -> AnalysisJob | None:
        return (
            self.db.query(AnalysisJob)
            .filter(
                AnalysisJob.id == job_id,
                AnalysisJob.organization_id == organization_id,
            )
            .first()
        )

    def get_job_with_result(
        self,
        job_id: uuid.UUID,
    ) -> AnalysisJob | None:
        return (
            self.db.query(AnalysisJob)
            .filter(AnalysisJob.id == job_id)
            .first()
        )

    def create_job(
        self,
        resume_id,
        organization_id,
    ):
        job = AnalysisJob(
            resume_id=resume_id,
            organization_id=organization_id,
            status=AnalysisJobStatus.PENDING,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def update_job_status(
        self,
        job_id,
        status,
    ):
        job = (
            self.db.query(AnalysisJob)
            .filter(AnalysisJob.id == job_id)
            .first()
        )

        if not job:
            return None

        job.status = status

        self.db.commit()
        self.db.refresh(job)

        return job

    def create_analysis_result(
        self,
        job_id,
        summary,
        skills,
        missing_skills,
        ats_score,
        raw_response,
    ):
        result = AnalysisResult(
            job_id=job_id,
            summary=summary,
            skills=skills,
            gaps=missing_skills,
            score=ats_score,
            raw_response=raw_response,
        )

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        slug: str,
    ):
        organization = Organization(
            name=name,
            slug=slug,
        )

        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return organization