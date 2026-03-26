from fastapi import APIRouter

from app.api.deps import AdminDep, CurrentUser, SessionDep
from app.schemas.user import UserAdminUpdate, UserPublic, UserUpdate
from app.services import user as user_service


router = APIRouter()

# Endpoint for getting all the users in the DB
# Can only be used by admins
@router.get("/", response_model=list[UserPublic])
def get_all_users(current_user: AdminDep, db: SessionDep):
    return user_service.get_all_users(db=db)

# Endpoint for getting the current user
@router.get("/me", response_model=UserPublic)
def get_current_user(current_user: CurrentUser):
    return current_user

# Endpoint for updating the current user
@router.patch("/me", response_model=UserPublic)
def update_user(current_user: CurrentUser, user_update: UserUpdate, db: SessionDep):
    return user_service.update_user(current_user=current_user, user_update=user_update, db=db)

# Endpoint for admins to update a specific user
@ router.patch("/admin/{user_id}", response_model=UserPublic)
def admin_update_user(user_id: int, user_update: UserAdminUpdate, current_user: AdminDep, db: SessionDep):
    current_user = user_service.get_user_by_id(user_id=user_id, db=db)
    return user_service.update_user(current_user=current_user, user_update=user_update, db=db)