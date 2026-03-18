from typing import Sequence
from sqlmodel import Session, select
from app.models import Seller
from app.schemas.seller import SellerAdminUpdate, SellerCreate, SellerUpdate

def get_all_sellers(db: Session) -> Sequence[Seller]:
    statement = select(Seller)
    return db.exec(statement).all()
    
def create_seller(seller_in: SellerCreate, user_id: int, db: Session) -> Seller:
    db_seller = Seller.model_validate(seller_in, update={"user_id": user_id})
    db.add(db_seller)
    db.flush()
    db.refresh(db_seller)
    return db_seller

def update_seller(current_seller: Seller, seller_update: SellerUpdate | SellerAdminUpdate, db: Session):
    update_data = seller_update.model_dump(exclude_unset=True)
    current_seller.sqlmodel_update(update_data)
    db.commit()
    db.refresh(current_seller)
    return current_seller

def get_seller_by_id(user_id: int, db: Session):
    statement = select(Seller).where(Seller.user_id == user_id)
    return db.exec(statement).one()

def delete_seller(user_id: int, db: Session):
    statement = select(Seller).where(Seller.user_id == user_id)
    seller = db.exec(statement).first()
    if seller:
        db.delete(seller)
        db.commit()