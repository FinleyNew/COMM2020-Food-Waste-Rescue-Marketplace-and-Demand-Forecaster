from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlmodel import Session
import jwt
from jwt.exceptions import InvalidTokenError

from app.db.session import engine
from app.core.config import settings
from app.core import security
from app.models.user import User
from app.models.seller import Seller
from app.models.consumer import Consumer
from app.schemas.token import TokenPayload

def get_db() -> Generator:
    # Open a new session
    with Session(engine) as session:
        yield session
    # As it is a generator the session automatically closes here

# This code is used to validate the JWT given from the user
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/login/access-token"
)

# This can be called in an endpoint and will get a session to be used for the duration of that endpoint
SessionDep = Annotated[Session, Depends(get_db)]

# This function is used to decrypt the token into a user_id and then get that user from the DB
def get_current_user(db: SessionDep, token: str = Depends(reusable_oauth2)) -> User:
    try:
        #Decode the JWT token using the secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code = 401,
            detail="Could not validate credentials",
        )
    
    if token_data.sub is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    #Find the user in the database using the ID from the token
    user = db.get(User, int(token_data.sub))
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")

    return user

# This can be called to get the current user using the token
CurrentUser = Annotated[User, Depends(get_current_user)]

# This function is used to get the current seller
# It uses the CurrentUser and then checks if their role is a seller or not
# If it is it gets that seller from the DB
def get_current_seller(db: SessionDep, current_user: CurrentUser) -> Seller:
    if current_user.role != "seller":
        raise HTTPException(status_code=400, detail="This user is not a seller")
    #Find the corresponding seller in the database
    seller = db.get(Seller, current_user.user_id)
    if not seller:
        raise HTTPException(status_code = 404, detail = "Seller not found")
    
    return seller

# This function is used to get the current consumer
# It uses the CurrentUser and then checks if their role is a consumer or not
# If it is it gets that consumer from the DB
def get_current_consumer(db: SessionDep, current_user: CurrentUser) -> Consumer:
    if current_user.role != "consumer":
        raise HTTPException(status_code=400, detail="This user is not a consumer")
    #Find the corresponding consumer in the database
    consumer_id = current_user.user_id
    if not consumer_id:
        raise HTTPException(status_code= 404, detail= "Consumer does not exist")
    consumer = db.get(Consumer, int(consumer_id))
    if not consumer:
        raise HTTPException(status_code = 404, detail = f"Consumer not found: {consumer_id}")
    
    return consumer

# This function is used to get the current admin
def get_current_admin(current_user: CurrentUser) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="This user is not an admin")
    return current_user

SellerDep = Annotated[Seller, Depends(get_current_seller)]
ConsumerDep = Annotated[Consumer, Depends(get_current_consumer)]
AdminDep = Annotated[User, Depends(get_current_admin)]