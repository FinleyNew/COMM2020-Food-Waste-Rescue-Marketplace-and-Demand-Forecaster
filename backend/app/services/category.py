from typing import Sequence
from sqlmodel import Session

from app.api.deps import SessionDep
from app.schemas.category import CategoryCreate
from app.models.bundlePosting import Category
from app.crud import category as category_crud


def create_category(category_in: CategoryCreate, db: Session) -> Category:
    return category_crud.create_category(category_in=category_in, db=db)

def get_all_categories(db: Session) -> Sequence[Category]:
    return category_crud.get_all_categories(db=db)