from fastapi import APIRouter, HTTPException
from app.api.deps import SellerDep, SessionDep
from app.schemas.forecast import ForecastPublic
from typing import List

router = APIRouter()

@router.get("/me", response_model= List[ForecastPublic])
def get_current_sellers_forecasts(current_seller: SellerDep, db: SessionDep):
    forecasts = current_seller.forecasts
    if not forecasts:
        raise HTTPException(status_code = 404, detail = "No forecasts found")
    return forecasts