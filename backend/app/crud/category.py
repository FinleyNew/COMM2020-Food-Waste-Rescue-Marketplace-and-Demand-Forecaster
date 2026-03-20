from typing import Sequence
from sqlmodel import Session, select

from app.models.bundlePosting import Category
from app.schemas.category import CategoryCreate


def get_all_categories(db: Session) -> Sequence[Category]:
    statement = select(Category)
    return db.exec(statement).all()

def create_category(category_in: CategoryCreate, db: Session) -> Category:
    db_category = Category.model_validate(category_in)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(category_id: int, db: Session):
    statement = select(Category).where(Category.category_id == category_id)
    category = db.exec(statement).first()
    if category:
        db.delete(category)
        db.commit()