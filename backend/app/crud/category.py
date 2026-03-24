from typing import Sequence
from sqlmodel import Session, select

from app.models.bundlePosting import Category
from app.schemas.category import CategoryCreate

# The crud function for creating a new category
def create_category(category_in: CategoryCreate, db: Session) -> Category:
    db_category = Category.model_validate(category_in)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# The crud function for getting all categories
def get_all_categories(db: Session) -> Sequence[Category]:
    statement = select(Category)
    return db.exec(statement).all()