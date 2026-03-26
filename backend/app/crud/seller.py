from typing import Sequence
from sqlmodel import Session, select
from app.models import Seller
from app.schemas.seller import SellerAdminUpdate, SellerCreate, SellerUpdate

# The crud function for getting all sellers
def get_all_sellers(db: Session) -> Sequence[Seller]:
    statement = select(Seller)
    return db.exec(statement).all()

# The crud function for creating a new seller
def create_seller(seller_in: SellerCreate, longitude: float | None, latitude: float | None, user_id: int, db: Session) -> Seller:
    db_seller = Seller.model_validate(seller_in, update={"user_id": user_id, "longitude": longitude, "latitude": latitude})
    db.add(db_seller)
    db.flush()
    db.refresh(db_seller)
    return db_seller

# The crud function for updating a seller
def update_seller(current_seller: Seller, seller_update: SellerUpdate | SellerAdminUpdate, db: Session):
    update_data = seller_update.model_dump(exclude_unset=True)
    current_seller.sqlmodel_update(update_data)
    db.commit()
    db.refresh(current_seller)
    return current_seller

# The crud function for getting a specific seller
def get_seller_by_id(user_id: int, db: Session):
    statement = select(Seller).where(Seller.user_id == user_id)
    return db.exec(statement).one()

# The crud function for deleting a specific seller
def delete_seller(user_id: int, db: Session):
    statement = select(Seller).where(Seller.user_id == user_id)
    seller = db.exec(statement).first()
    if seller:
        db.delete(seller)
        db.commit()