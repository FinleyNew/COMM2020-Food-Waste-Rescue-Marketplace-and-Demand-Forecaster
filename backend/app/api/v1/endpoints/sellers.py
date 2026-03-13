from fastapi import APIRouter
from app.api.deps import AdminDep, SellerDep, SessionDep
from app.schemas.seller import SellerAdminUpdate, SellerCreate, SellerPublic, SellerUpdate
from app.services import seller as seller_service
from app.schemas.user import UserCreate

router = APIRouter()

#Endpoint for getting the current seller
@router.get("/me", response_model=SellerPublic)
def get_current_seller(current_seller: SellerDep):
    return current_seller

# Ednpoint for creating a new seller
@router.post("/", response_model = SellerPublic)
def create_seller(seller_in: SellerCreate, user_in: UserCreate, db: SessionDep):
    return seller_service.create_seller(seller_in=seller_in, user_in=user_in, db=db)

@router.patch("/me", response_model=SellerPublic)
def update_seller(current_seller: SellerDep, seller_update: SellerUpdate, db: SessionDep):
    return seller_service.update_seller(current_seller=current_seller, seller_update=seller_update, db=db)

@router.patch("/admin/{user_id}", response_model=SellerPublic)
def admin_update_seller(user_id: int, seller_update: SellerAdminUpdate, current_user: AdminDep, db: SessionDep):
    current_seller = seller_service.get_seller_by_id(user_id=user_id, db=db)
    return seller_service.update_seller(current_seller=current_seller, seller_update=seller_update, db=db)

@router.delete("/me")
def delete_current_seller(current_user: SellerDep, db: SessionDep):
    seller_service.delete_seller(user_id=current_user.user_id, db=db) # type: ignore

@router.delete("/{user_id}")
def delete_seller(user_id: int, current_user: AdminDep, db: SessionDep):
    seller_service.delete_seller(user_id=user_id, db=db)