from fastapi import APIRouter, Form
from app.api.deps import AdminDep, SellerDep, SessionDep
from app.schemas.seller import SellerAdminUpdate, SellerCreate, SellerPublic, SellerUpdate
from app.services import seller as seller_service
from fastapi import UploadFile, File
from app.schemas.user import UserCreate
from app.services.cloudinary import upload_image
from app.schemas.analytics import SellerAnalyticsSummary
from app.services import analytics as analytics_service

router = APIRouter()

@router.get("/", response_model=list[SellerPublic])
def get_all_sellers(current_user: AdminDep, db: SessionDep):
    return seller_service.get_all_sellers(db=db)

#Endpoint for getting the current seller
@router.get("/me", response_model=SellerPublic)
def get_current_seller(current_seller: SellerDep):
    return current_seller

# Ednpoint for creating a new seller
@router.post("/", response_model=SellerPublic)
async def create_seller(
    db: SessionDep,
    name: str = Form(...),
    location: str = Form(...),
    opening_hours: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(None),
):
    logo_url = "https://res.cloudinary.com/dnbeji59a/image/upload/v1774196127/profile-picture-blank_nnm3vq.jpg"
    if file:
        logo_url = await upload_image(await file.read())

    seller_in = SellerCreate(name=name, location=location, opening_hours=opening_hours, logo_url=logo_url)
    user_in = UserCreate(email=email, password=password)

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

@router.get("/me/analytics/summary", response_model=SellerAnalyticsSummary)
def get_seller_analytics_summary(current_seller: SellerDep, db: SessionDep):
    return analytics_service.get_seller_analytics_summary(seller_id=current_seller.user_id, db=db)