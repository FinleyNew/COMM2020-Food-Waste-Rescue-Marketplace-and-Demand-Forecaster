from fastapi import APIRouter, HTTPException
from app.api.deps import SellerDep, SessionDep
from app.schemas.record import RecordPublic
from typing import List

router = APIRouter()

# Endpoint for getting the current sellers records
@router.get("/me", response_model= List[RecordPublic])
def get_current_sellers_records(current_seller: SellerDep, db: SessionDep):
    return current_seller.records or []