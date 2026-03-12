from sqlmodel import Session
from app.models.user import User
from app.crud import user as user_crud
from app.schemas.user import UserUpdate
from app.core.security import get_password_hash


def get_user_by_email(email: str, db: Session) -> User | None:
    return user_crud.get_user_by_email(email=email, db=db)

def get_user_by_id(user_id: int, db: Session) -> User:
    return user_crud.get_user_by_id(user_id=user_id, db=db)

def update_user(current_user: User, user_update: UserUpdate, db: Session) -> User:
    if user_update.password:
        user_update.password = get_password_hash(user_update.password)
    return user_crud.update_user(current_user=current_user, user_update=user_update, db=db)