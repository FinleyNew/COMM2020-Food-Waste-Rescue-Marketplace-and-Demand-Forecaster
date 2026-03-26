from typing import Sequence
from fastapi import HTTPException
from sqlmodel import Session
import httpx

from app.schemas.seller import SellerAdminUpdate, SellerCreate, SellerUpdate
from app.schemas.user import UserCreate
from app.models.seller import Seller
from app.crud import user as user_crud
from app.crud import seller as seller_crud
from app.core.security import get_password_hash
from app.models.enums import Role

# Gets all the sellers
def get_all_sellers(db: Session) -> Sequence[Seller]:
    return seller_crud.get_all_sellers(db=db)

# Creates a new seller
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
        # Get the seller's coordinates
        coords = get_coordinates(seller_in.location)
        latitude, longitude = coords if coords else (None, None)
        # Create a new consumer with that Id
        
        seller = seller_crud.create_seller(seller_in=seller_in, user_id=user_id, longitude=longitude, latitude=latitude, db=db)
        db.commit()
        db.refresh(seller)
        return seller
    except Exception:
        db.rollback
        raise

# Gets the coordinates from the Entered postcode
def get_coordinates(address: str) -> tuple[float, float] | None:
    parts = address.split()
    if len(parts) < 2:
        raise ValueError(f"Address too short to extract postcode: {address!r}")

    postcode = f"{parts[-2]} {parts[-1]}"

    try:
        with httpx.Client() as client:
            response = client.get(f"https://api.postcodes.io/postcodes/{postcode}")
            data = response.json()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Request to postcodes.io failed: {e}") from e

    if data.get("status") != 200:
        return None

    try:
        return data["result"]["latitude"], data["result"]["longitude"]
    except KeyError:
        raise RuntimeError(f"Unexpected response shape from postcodes.io: {data}")

# Updates seller
def update_seller(current_seller: Seller, seller_update: SellerUpdate | SellerAdminUpdate, db: Session):
    return seller_crud.update_seller(current_seller=current_seller, seller_update=seller_update, db=db)

# Gets seller by their ID
def get_seller_by_id(user_id: int, db: Session) -> Seller:
    return seller_crud.get_seller_by_id(user_id=user_id, db=db)

# Deletes a specified seller
def delete_seller(user_id: int, db: Session):
    seller_crud.delete_seller(user_id=user_id, db=db)
    user_crud.delete_user(user_id=user_id, db=db)