from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import UUID

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

load_dotenv()
import os

print("MAIN DATABASE_URL =", os.getenv("DATABASE_URL"))
print("MAIN POSTGRES_USER =", os.getenv("POSTGRES_USER"))

app = FastAPI(title="ARA Backend", version="0.1.0")


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