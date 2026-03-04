from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from app.services import user as user_service
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from app.api.deps import SessionDep


router = APIRouter()

#No login system implemented yet

@router.post("/access-token", response_model = Token)
def access_token(db: SessionDep, form: OAuth2PasswordRequestForm = Depends()):
    user = user_service.get_user_by_email(email = form.username, db=db)
    if not user or not security.verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    token = security.create_access_token(user.user_id)

    return {"access_token": token, "token_type": "bearer"}