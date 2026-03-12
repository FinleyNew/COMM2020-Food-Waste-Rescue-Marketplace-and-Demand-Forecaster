from fastapi import HTTPException
from sqlmodel import Session

from app.schemas.seller import SellerCreate
from app.schemas.user import UserCreate
from app.models.seller import Seller
from app.crud import user as user_crud
from app.crud import seller as seller_crud
from app.core.security import get_password_hash
from app.models.enums import Role


def create_seller(seller_in: SellerCreate, user_in: UserCreate, db: Session) -> Seller:
    #Check if email already exists
    if user_crud.get_user_by_email(email=user_in.email, db=db):
        raise HTTPException(status_code=400, detail="This email is already registered")
    try:
        # Hash password
        hashed_password = get_password_hash(password=user_in.password)
        #Create a new user
        user = user_crud.create_user(user_in=user_in, hashed_password=hashed_password, role=Role.SELLER, db=db)
        #Get that users Id
        user_id = user.user_id
        if not user_id:
            raise HTTPException(status_code=404, detail="Could not get userID")
        #Create a new consumer with that Id
        seller = seller_crud.create_seller(seller_in=seller_in, user_id=user_id, db=db)
        db.commit()
        db.refresh(seller)
        return seller
    except Exception:
        db.rollback
        raise
