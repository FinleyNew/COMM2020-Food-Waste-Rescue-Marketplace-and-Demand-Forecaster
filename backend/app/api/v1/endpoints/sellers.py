from fastapi import APIRouter, Form
from app.api.deps import AdminDep, SellerDep, SessionDep
from app.schemas.seller import SellerAdminUpdate, SellerCreate, SellerPublic, SellerUpdate
from app.services import seller as seller_service
from fastapi import UploadFile, File
from app.schemas.user import UserCreate
from app.services.cloudinary import upload_image
from app.schemas.analytics import DiscountBandMetrics, SellerAnalyticsSummary, SellerOperationalInsights, SellerSellThroughBreakdown
from app.services import analytics as analytics_service

router = APIRouter()

# Endpoint for getting all sellers in the DB
# Can only be used by admins
@router.get("/", response_model=list[SellerPublic])
def get_all_sellers(current_user: AdminDep, db: SessionDep):
    return seller_service.get_all_sellers(db=db)

#Endpoint for getting the current seller
@router.get("/me", response_model=SellerPublic)
def get_current_seller(current_seller: SellerDep):
    return current_seller

# Endpoint for creating a new seller
# Due to sellers also taking a profile picture the arguments are different
# Image data can not be sent in JSON so we use a Form
# Is async as as it has to wait for the API response
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
    # Use standard logo
    logo_url = "https://res.cloudinary.com/dnbeji59a/image/upload/v1774196127/profile-picture-blank_nnm3vq.jpg"
    # If image is provided use that instead
    if file:
        logo_url = await upload_image(await file.read())

    # Create the seller and user classes from the provided info
    seller_in = SellerCreate(name=name, location=location, opening_hours=opening_hours, logo_url=logo_url)
    user_in = UserCreate(email=email, password=password)

    return seller_service.create_seller(seller_in=seller_in, user_in=user_in, db=db)

# Endpoint for updating the current seller
@router.patch("/me", response_model=SellerPublic)
def update_seller(current_seller: SellerDep, seller_update: SellerUpdate, db: SessionDep):
    return seller_service.update_seller(current_seller=current_seller, seller_update=seller_update, db=db)

# Endpoint for admins to update a specific seller
@router.patch("/admin/{user_id}", response_model=SellerPublic)
def admin_update_seller(user_id: int, seller_update: SellerAdminUpdate, current_user: AdminDep, db: SessionDep):
    current_seller = seller_service.get_seller_by_id(user_id=user_id, db=db)
    return seller_service.update_seller(current_seller=current_seller, seller_update=seller_update, db=db)

# Endpoint for a seller to delete their own account
@router.delete("/me")
def delete_current_seller(current_user: SellerDep, db: SessionDep):
    seller_service.delete_seller(user_id=current_user.user_id, db=db) # type: ignore

# Endpoint for deleting a specific users account
# Can only be used by admins
@router.delete("/{user_id}")
def delete_seller(user_id: int, current_user: AdminDep, db: SessionDep):
    seller_service.delete_seller(user_id=user_id, db=db)

# Endpoint for getting the current sellers analytics summary
@router.get("/me/analytics/summary", response_model=SellerAnalyticsSummary)
def get_seller_analytics_summary(current_seller: SellerDep, db: SessionDep):
    return analytics_service.get_seller_analytics_summary(seller_id=current_seller.user_id, db=db) # type: ignore

# Endpoint for getting the current sellers sell through breakdown
@router.get("/me/analytics/sell-through-breakdown", response_model=SellerSellThroughBreakdown)
def get_seller_sell_through_breakdown(current_seller: SellerDep, db: SessionDep):
    return analytics_service.get_seller_sell_through_breakdown(seller_id=current_seller.user_id, db=db) # type: ignore

# Endpoint for getting the current sellers pricing effectiveness
@router.get("/me/analytics/pricing-effectiveness", response_model=list[DiscountBandMetrics])
def get_seller_pricing_effectiveness(current_seller: SellerDep, db: SessionDep):
    return analytics_service.get_seller_pricing_effectiveness(seller_id=current_seller.user_id, db=db) # type: ignore

# Endpoint for getting the current sellers operational insights
@router.get("/me/analytics/operational-insights", response_model=SellerOperationalInsights)
def get_seller_operational_insights(current_seller: SellerDep, db: SessionDep):
    return analytics_service.get_seller_operational_insights(seller_id=current_seller.user_id, db=db) # type: ignore