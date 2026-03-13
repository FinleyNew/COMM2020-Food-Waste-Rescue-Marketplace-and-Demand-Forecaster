from fastapi import APIRouter, HTTPException
from app.api.deps import AdminDep, SellerDep, SessionDep
from app.schemas.forecast import ForecastPublic
from app.services import forecast as forecast_service
from typing import List
from app.schemas.bundlePosting import BundlePostingCreate

router = APIRouter()

# Endpoint for getting the current sellers forecasts
@router.get("/me", response_model= List[ForecastPublic])
def get_current_sellers_forecasts(current_seller: SellerDep, db: SessionDep):
    return current_seller.forecasts or []

@router.get("/", response_model=list[ForecastPublic])
def get_all_forecasts(current_user: AdminDep, db: SessionDep):
    return forecast_service.get_all_forecasts(db=db)

# Endpoint for getting the predicted sales and no show for a given BundlepostingCreate input
@router.post("/", response_model=ForecastPublic)
def get_new_forecast(bundle_in: BundlePostingCreate, db: SessionDep):
    forecast = forecast_service.get_forecast(bundle_in=bundle_in, db=db)
    if not forecast:
        raise HTTPException(status_code=404, detail="No forecast made")
    return forecast

@router.delete("/{forecast_id}")
def delete_forecast(forecast_id: int, current_user: AdminDep, db: SessionDep):
    forecast_service.delete_forecast(forecast_id=forecast_id, db=db)