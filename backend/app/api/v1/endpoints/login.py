from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services import user


router = APIRouter()

#No login system implemented yet

@router.post("/access-token")
def access_token(form: OAuth2PasswordRequestForm = Depends()):
    user = user.get_user(form.username)