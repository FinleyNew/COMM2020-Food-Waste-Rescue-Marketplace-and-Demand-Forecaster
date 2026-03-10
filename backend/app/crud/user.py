from app.models.user import User
from sqlmodel import Session, select

from app.schemas.user import UserCreate

def get_user_by_email(email: str, db: Session) -> User | None:
    statement = select(User).where(User.email == email)
    return db.exec(statement).one_or_none()

def create_user(user_in: UserCreate, hashed_password: str, db: Session) -> User:
    db_user = User.model_validate(user_in, update={"password": hashed_password})
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user