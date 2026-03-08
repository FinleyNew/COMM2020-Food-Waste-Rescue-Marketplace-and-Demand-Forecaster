from fastapi import APIRouter

from app.api.deps import CurrentUser, SessionDep
from app.schemas.user import UserPublic


router = APIRouter()

@router.get("/me", response_model=UserPublic)
def get_current_user(current_user: CurrentUser, db: SessionDep):
    return current_user