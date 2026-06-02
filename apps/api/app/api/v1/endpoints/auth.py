import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import UserRepository
from app.schemas import TokenResponse, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
def register(_payload: UserCreate, _db: Session = Depends(get_db)) -> UserResponse:
    """Register a new user and organization."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
def login(_db: Session = Depends(get_db)) -> TokenResponse:
    """Authenticate and return JWT."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


def get_current_user_id() -> uuid.UUID:
    """Dependency placeholder — replace with JWT validation."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Auth not implemented")


def get_current_user(db: Session = Depends(get_db)):
    user_id = get_current_user_id()
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user
