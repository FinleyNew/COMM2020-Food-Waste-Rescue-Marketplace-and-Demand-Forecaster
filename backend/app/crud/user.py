from app.models.user import User
from sqlmodel import Session, select

def get_user_by_email(email: str, db: Session) -> User:
    statement = select(User).where(User.email == email)
    return db.exec(statement).one()