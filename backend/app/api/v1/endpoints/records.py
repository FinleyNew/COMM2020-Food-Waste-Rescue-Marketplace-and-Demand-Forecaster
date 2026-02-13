from fastapi import APIRouter, HTTPException
from app.api.deps import SellerDep, SessionDep
from app.schemas.record import RecordPublic
from typing import List

router = APIRouter()

# Endpoint for getting the current sellers records
@router.get("/me", response_model= List[RecordPublic])
def get_current_sellers_records(current_seller: SellerDep, db: SessionDep):
    records = current_seller.records
    if not records:
        raise HTTPException(status_code = 404, detail = "No records found")
    return records