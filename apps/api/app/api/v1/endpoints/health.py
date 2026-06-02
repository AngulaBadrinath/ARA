from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str | bool]:
    db_ok = False
    try:
        db: Session = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_ok = True
    except Exception:
        pass
    return {"status": "ready" if db_ok else "degraded", "database": db_ok}
