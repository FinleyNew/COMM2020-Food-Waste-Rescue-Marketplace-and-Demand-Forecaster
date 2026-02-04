from fastapi import APIRouter
from app.api.deps import SellerDep, SessionDep
from app.schemas.bundle import BundleCreate, BundlePublic
from app.services.bundle import bundle as bundle_service

router = APIRouter()

@router.post("/", response_model = BundlePublic)
def create_bundle(bundle_in: BundleCreate, current_seller: SellerDep, db: SessionDep):
    #Call bundle_service

@router.get("/", response_model = BundlePublic)
def get_active_bundles(db: SessionDep):
    #Call bundle_service

@router.get("/me", response_model = list[BundlePublic])
def get_current_sellers_bundles(current_seller: SellerDep, db: SessionDep):
    #Call bundle_service with sellers ID

@router.get("/{bundle_id}", response_model = BundlePublic)
def get_bundle(bundle_id: int, db: SessionDep):
    #Call bundle_service with bundle_id

@router.delete("/{bundle_id}")
def delete_bundle(bundle_id: int, db: SessionDep)
    #Call bundle_service