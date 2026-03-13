from typing import Sequence

from app.models.user import User
from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserUpdate
from app.models.enums import Role

def get_all_users(db: Session) -> Sequence[User]:
    statement = select(User)
    return db.exec(statement).all()

def get_user_by_email(email: str, db: Session) -> User | None:
    statement = select(User).where(User.email == email)
    return db.exec(statement).one_or_none()

def create_user(user_in: UserCreate, hashed_password: str, role: Role, db: Session) -> User:
    db_user = User.model_validate(user_in, update={"password": hashed_password, "role": role})
    db.add(db_user)
    db.flush()
    db.refresh(db_user)
    return db_user

def get_user_by_id(user_id: int, db: Session) -> User:
    statement = select(User).where(User.user_id == user_id)
    return db.exec(statement).one()

def update_user(current_user: User, user_update: UserUpdate, db: Session) -> User:
    update_data = user_update.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(update_data)
    db.commit()
    db.refresh(current_user)
    return current_user

def delete_user(user_id: int, db: Session):
    statement = select(User).where(User.user_id == user_id)
    user = db.exec(statement).first()
    if user:
        db.delete(user)
        db.commit()