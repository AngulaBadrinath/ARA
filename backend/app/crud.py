from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.models import Organization, User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_organization(
    db: Session,
    name: str,
    slug: str,
):
    org = Organization(
        name=name,
        slug=slug,
    )

    db.add(org)
    db.commit()
    db.refresh(org)

    return org


def get_organizations(db: Session):
    return db.query(Organization).all() 


def create_user(
    db: Session,
    organization_id,
    email: str,
    password: str,
    full_name: str,
):
    user = User(
        organization_id=organization_id,
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id):
    return db.query(User).filter(User.id == user_id).first()