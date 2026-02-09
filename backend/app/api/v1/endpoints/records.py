from fastapi import APIRouter
from app.api.deps import SellerDep, SessionDep
from app.schemas.record import RecordPublic

router = APIRouter()

@router.get("/me", response_model= RecordPublic)
def get_current_sellers_records(current_seller: SellerDep, db: SessionDep):
    return current_seller.records