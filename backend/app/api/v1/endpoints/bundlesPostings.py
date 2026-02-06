from fastapi import APIRouter
from app.api.deps import SellerDep, SessionDep
from backend.app.schemas.bundlePosting import BundlePostingCreate, BundlePostingPublic
from backend.app.services import bundlePosting as posting_service

router = APIRouter()

@router.post("/", response_model = BundlePostingPublic)
def create_posting(bundle_in: BundlePostingCreate, current_seller: SellerDep, db: SessionDep):
    #Call bundle_service

@router.get("/", response_model = list[BundlePostingPublic])
def get_active_bundles(db: SessionDep):
    #Call bundle_service

@router.get("/me", response_model = list[BundlePostingPublic])
def get_current_sellers_bundles(current_seller: SellerDep, db: SessionDep):
    # return current_seller.posting

@router.get("/{posting_id}", response_model = BundlePostingPublic)
def get_bundle(bundle_id: int, db: SessionDep):
    #Call bundle_service with bundle_id

@router.delete("/{posting_id}")
def delete_bundle(bundle_id: int, db: SessionDep)
    #Call bundle_service