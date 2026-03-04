from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from app.services import user as user_service
from app.core.security import ALGORITHM
from app.core.config import settings
from app.schemas.token import Token


router = APIRouter()

#No login system implemented yet

@router.post("/access-token", response_model = Token)
def access_token(form: OAuth2PasswordRequestForm = Depends()):
    user = user_service.get_user(form.username)
    if not user or not settings.pwd_context.verify(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    token = jwt.encode(
        {"sub": str(user.user_id), "exp": datetime.now(timezone.utc) + timedelta(hours=8)},
        settings.SECRET_KEY, algorithm=ALGORITHM
    )

    return {"access_token": token, "token_type": "bearer"}