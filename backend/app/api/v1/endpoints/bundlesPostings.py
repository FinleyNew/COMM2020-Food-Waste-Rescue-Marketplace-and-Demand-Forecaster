from fastapi import APIRouter
from app.api.deps import SellerDep, SessionDep
from backend.app.schemas.bundlePosting import BundlePostingCreate, BundlePostingPublic
from backend.app.services import bundlePosting as bundle_posting_service

router = APIRouter()

@router.post("/", response_model = BundlePostingPublic)
def create_posting(bundle_in: BundlePostingCreate, current_seller: SellerDep, db: SessionDep):
    user_id = current_seller.user_id
    if user_id:
        return bundle_posting_service.create_bundle_posting(
            bundle_in=bundle_in,
            owner_id=user_id,
            db=db
        )

@router.get("/", response_model = list[BundlePostingPublic])
def get_active_bundles(db: SessionDep):
    return bundle_posting_service.get_active_bundle_postings(db=db)

@router.get("/me", response_model = list[BundlePostingPublic])
def get_current_sellers_bundles(current_seller: SellerDep, db: SessionDep):
    return current_seller.postings

@router.get("/{posting_id}", response_model = BundlePostingPublic)
def get_bundle(posting_id: int, db: SessionDep):
    bundle_posting_service.get_bundle_posting(
        posting_id=posting_id,
        db=db
    )

@router.delete("/{posting_id}")
def delete_bundle(posting_id: int, db: SessionDep):
    bundle_posting_service.delete_bundle_posting(posting_id=posting_id, db=db)