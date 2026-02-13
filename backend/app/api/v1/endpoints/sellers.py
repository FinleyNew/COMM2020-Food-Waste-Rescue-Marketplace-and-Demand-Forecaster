from fastapi import APIRouter
from app.api.deps import SellerDep, SessionDep
from app.schemas.seller import SellerPublic
from app.services import seller as seller_service

router = APIRouter()

# Currently not in use