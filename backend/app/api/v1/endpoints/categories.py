
from fastapi import APIRouter

from app.schemas.category import CategoryCreate, CategoryPublic
from app.api.deps import AdminDep, SessionDep
from app.services import category as category_service


router = APIRouter()

# Endpoint for creating a new category
# Only admins can do this
@router.post("/", response_model=CategoryPublic)
def create_category(category_in: CategoryCreate, current_user: AdminDep, db: SessionDep):
    return category_service.create_category(category_in=category_in, db=db)

# Endpoint for getting all the categories
@router.get("/", response_model=list[CategoryPublic])
def get_all_categories(db: SessionDep):
    return category_service.get_all_categories(db=db)