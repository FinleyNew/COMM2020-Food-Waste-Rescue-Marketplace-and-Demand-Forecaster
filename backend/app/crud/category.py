from typing import Sequence
from sqlmodel import Session, select

from app.models.bundlePosting import Category


def get_all_categories(db: Session) -> Sequence[Category]:
    statement = select(Category)
    return db.exec(statement).all()