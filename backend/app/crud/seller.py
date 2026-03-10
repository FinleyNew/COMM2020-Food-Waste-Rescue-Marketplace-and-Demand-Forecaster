from sqlmodel import Session, select
from app.models import Seller
from app.schemas.seller import SellerCreate

def create_seller(seller_in: SellerCreate, user_id: int, db: Session) -> Seller:
    db_seller = Seller.model_validate(seller_in, update={"user_id": user_id})
    db.add(db_seller)
    db.flush()
    db.refresh(db_seller)
    return db_seller