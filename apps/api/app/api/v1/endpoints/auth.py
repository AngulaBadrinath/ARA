import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

from app.models import User

from app.repositories import (
    UserRepository,
    OrganizationRepository,
)

from app.schemas import (
    UserCreate,
    UserResponse,
    TokenResponse,
    LoginRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    user_repo = UserRepository(db)

    existing_user = user_repo.get_by_email(payload.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    org_repo = OrganizationRepository(db)

    slug = payload.organization_name.lower().strip().replace(" ", "-")

    organization = org_repo.get_by_slug(slug)

    if organization is None:
        organization = org_repo.create(
            name=payload.organization_name,
            slug=slug,
        )

    user = User(
        organization_id=organization.id,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )

    return user_repo.create(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    user = UserRepository(db).get_by_email(
        payload.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
        payload.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        str(user.id)
    )

    return TokenResponse(
        access_token=token
    )

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> uuid.UUID:

    print("TOKEN:", credentials.credentials)

    payload = decode_access_token(
        credentials.credentials
    )

    print("PAYLOAD:", payload)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return uuid.UUID(payload["sub"])


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(credentials)

    user = UserRepository(db).get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    return user

@router.get("/me")
def me(
    current_user = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "organization_id": str(current_user.organization_id),
    }

