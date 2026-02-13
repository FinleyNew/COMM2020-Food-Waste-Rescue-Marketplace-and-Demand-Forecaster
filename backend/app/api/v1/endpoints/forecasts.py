from fastapi import APIRouter, HTTPException
from app.api.deps import SellerDep, SessionDep
from app.schemas.forecast import ForecastPublic
from app.services.forecast import get_forecast
from typing import List
from app.schemas.bundlePosting import BundlePostingCreate

router = APIRouter()

# Endpoint for getting the current sellers forecasts
@router.get("/me", response_model= List[ForecastPublic])
def get_current_sellers_forecasts(current_seller: SellerDep, db: SessionDep):
    forecasts = current_seller.forecasts
    if not forecasts:
        raise HTTPException(status_code = 404, detail = "No forecasts found")
    return forecasts

# Endpoint for getting the predicted sales and no show for a given BundlepostingCreate input
@router.post("/", response_model=ForecastPublic)
def get_new_forecast(bundle_in: BundlePostingCreate, db: SessionDep):
    forecast = get_forecast(bundle_in=bundle_in, db=db)
    if not forecast:
        raise HTTPException(status_code=404, detail="No forecast made")
    return forecast