from typing import Sequence
from fastapi import HTTPException
from sqlmodel import Session
from app.models.user import User
from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.models.enums import Role

# Creates a new admin
def create_admin(user_in: UserCreate, db: Session) -> User:
    if user_crud.get_user_by_email(email=user_in.email, db=db):
        raise HTTPException(status_code=400, detail="This email is already registered")
    try:
        hashed_password = get_password_hash(password=user_in.password)
        user = user_crud.create_user(user_in=user_in, hashed_password=hashed_password, role=Role.ADMIN, db=db)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback
        raise

# Gets all users
def get_all_users(db: Session) -> Sequence[User]:
    return user_crud.get_all_users(db=db)

# Gets a specific user by their email
def get_user_by_email(email: str, db: Session) -> User | None:
    return user_crud.get_user_by_email(email=email, db=db)

# Gets a specific user by their ID
def get_user_by_id(user_id: int, db: Session) -> User:
    return user_crud.get_user_by_id(user_id=user_id, db=db)

# Updates user
def update_user(current_user: User, user_update: UserUpdate, db: Session) -> User:
    if user_update.password:
        user_update.password = get_password_hash(user_update.password)
    return user_crud.update_user(current_user=current_user, user_update=user_update, db=db)