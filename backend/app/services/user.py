
# def create_new_user():

# def authenticate_user():

from sqlmodel import Session
from app.models.user import User
from app.crud import user as user_crud


def get_user_by_email(email: str, db: Session) -> User:
    return user_crud.get_user_by_email(email=email, db=db)