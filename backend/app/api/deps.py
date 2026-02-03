from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlmodel import Session

from app.db.session import engine
from app.core.config import settings
from app.core import security
from app.models.user import User
from app.models.seller import Seller
from app.models.consumer import Consumer
from app.schemas.token import TokenPayload


def get_db() -> Generator:
    # Open a new "session" (a single conversation with the DB)
    with Session(engine) as session:
        yield session
    # Once the request is finished, the session automatically closes here.
    
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR}/login/access-token"
)

SessionDep = Annotated[Session, Depends(get_db)]

def get_current_user(db: SessionDep, token: str = Depends(reusable_oauth2) -> User:

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_seller(current_user: CurrentUser) -> Seller:

def get_current_consumer(current_user: CurrentUser) -> Consumer:

def get_current_admin(current_user: CurrentUser) -> User:

SellerDep = Annotated[Seller, Depends(get_current_seller)]
ConsumerDep = Annotated[Consumer, Depends(get_current_consumer)]
AdminDep = Annotated[User, Depends(get_current_admin)]