from fastapi import APIRouter
from app.api.deps import SellerDep, SessionDep
from app.schemas.seller import SellerCreate, SellerPublic
from app.services import seller as seller_service
from app.schemas.user import UserCreate

router = APIRouter()

# Ednpoint for creating a new seller
@router.post("/", response_model = SellerPublic)
def create_seller(seller_in: SellerCreate, user_in: UserCreate, db: SessionDep):
    return seller_service.create_seller(seller_in=seller_in, user_in=user_in, db=db)