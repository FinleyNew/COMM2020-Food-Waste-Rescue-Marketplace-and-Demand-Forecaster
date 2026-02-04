from fastapi import APIRouter
from app.api.deps import SellerDep, ConsumerDep, SessionDep
from app.schemas.reservation import ReservationPublic

router = APIRouter()