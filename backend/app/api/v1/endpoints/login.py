from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.services import user as user_service
from app.core import security
from app.schemas.token import Token
from app.api.deps import SessionDep


router = APIRouter()

# Endpoint for getting the access token
# It ensures the username and password match and only returns the JWT if they do
@router.post("/access-token", response_model = Token)
def access_token(db: SessionDep, form: OAuth2PasswordRequestForm = Depends()):
    user = user_service.get_user_by_email(email = form.username, db=db)
    if not user or not security.verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    user_id = user.user_id
    if not user_id:
        raise HTTPException(status_code=404, detail="user id not found")
    token = security.create_access_token(user_id)

    return {"access_token": token, "token_type": "bearer"}