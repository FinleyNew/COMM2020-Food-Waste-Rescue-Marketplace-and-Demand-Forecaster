from fastapi import APIRouter
from app.api.deps import SellerDep, SessionDep
from app.schemas.forecast import ForecastPublic

router = APIRouter()

@router.get("me", response_model= ForecastPublic)
def get_current_sellers_forecasts(current_seller: SellerDep, db: SessionDep):
    return current_seller.forecasts