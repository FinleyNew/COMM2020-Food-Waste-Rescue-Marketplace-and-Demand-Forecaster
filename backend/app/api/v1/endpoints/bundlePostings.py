from fastapi import APIRouter, HTTPException
from app.api.deps import SellerDep, SessionDep
from app.schemas.bundlePosting import BundlePostingCreate, BundlePostingPublic
from app.services import bundlePosting as bundle_posting_service

router = APIRouter()

# Endpoint for creating a posting
@router.post("/", response_model = BundlePostingPublic)
def create_posting(bundle_in: BundlePostingCreate, current_seller: SellerDep, db: SessionDep):
    user_id = current_seller.user_id
    if user_id:
        return bundle_posting_service.create_bundle_posting(
            bundle_in=bundle_in,
            owner_id=user_id,
            db=db
        )

# Endpoint for getting all available bundles
@router.get("/", response_model = list[BundlePostingPublic])
def get_active_bundles(db: SessionDep):
    bundle_postings = bundle_posting_service.get_active_bundle_postings(db=db)
    if not bundle_postings:
        raise HTTPException(status_code=404, detail="No active bundles found")
    return bundle_postings

# Endpoint for getting all bundles
@router.get("/all", response_model = list[BundlePostingPublic])
def get_all_bundles(db: SessionDep):
    bundle_postings = bundle_posting_service.get_all_bundle_postings(db=db)
    if not bundle_postings:
        raise HTTPException(status_code=404, detail="No bundles found")
    return bundle_postings

# Endpoint for getting the current sellers bundles
@router.get("/me", response_model = list[BundlePostingPublic])
def get_current_sellers_bundles(current_seller: SellerDep, db: SessionDep):
    postings = current_seller.postings
    if not postings:
        raise HTTPException(status_code=404, detail="No bundles found")
    return postings

# Endpoint for getting a specific bundle posting
@router.get("/{posting_id}", response_model = BundlePostingPublic)
def get_bundle(posting_id: int, db: SessionDep):
    bundle = bundle_posting_service.get_bundle_posting(
        posting_id=posting_id,
        db=db
    )
    if bundle is None:
        raise HTTPException(status_code=404, detail="Bundle not found")
    return bundle

# Endpoint for deleting a specific bundle
# Currently not in use
@router.delete("/{posting_id}")
def delete_bundle(posting_id: int, db: SessionDep):
    bundle_posting_service.delete_bundle_posting(posting_id=posting_id, db=db)