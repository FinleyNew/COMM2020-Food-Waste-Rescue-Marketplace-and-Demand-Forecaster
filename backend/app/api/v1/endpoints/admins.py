import json
import os

from fastapi import APIRouter, HTTPException

from app.api.deps import AdminDep, SessionDep
from app.schemas.user import UserCreate, UserPublic
from app.services import user as user_service


router = APIRouter()

@router.get("/tests")
def get_test_results(admin: AdminDep):
    if not os.path.exists("test_results.json"):
        raise HTTPException(status_code=404, detail="No test results available yet")
    with open("test_results.json") as f:
        return json.load(f)


# Endpoint for creating a new admin
@router.post("/", response_model=UserPublic)
def create_admin(user_in: UserCreate, admin: AdminDep, db: SessionDep):
    return user_service.create_admin(user_in=user_in, db=db)