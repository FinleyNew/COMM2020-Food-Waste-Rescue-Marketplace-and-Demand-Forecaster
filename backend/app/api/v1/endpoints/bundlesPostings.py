from fastapi import APIRouter, HTTPException
from app.api.deps import AdminDep, SellerDep, SessionDep
from app.schemas.bundlePosting import BundlePostingAdminUpdate, BundlePostingCreate, BundlePostingPublic, BundlePostingUpdate
from app.services import bundlePosting as bundle_posting_service

router = APIRouter()

# Endpoint for creating a new posting
@router.post("/", response_model = BundlePostingPublic)
def create_posting(bundle_in: BundlePostingCreate, current_seller: SellerDep, db: SessionDep):
    user_id = current_seller.user_id
    if user_id:
        return bundle_posting_service.create_bundle_posting(
            bundle_in=bundle_in,
            owner_id=user_id,
            db=db
        )

# Endpoint for getting all available bundles postings
@router.get("/", response_model = list[BundlePostingPublic])
def get_active_bundles(db: SessionDep):
    bundle_postings = bundle_posting_service.get_active_bundle_postings(db=db)
    return bundle_postings or []

# Endpoint for getting all bundle postings
@router.get("/all", response_model = list[BundlePostingPublic])
def get_all_bundles(current_user: AdminDep, db: SessionDep):
    bundle_postings = bundle_posting_service.get_all_bundle_postings(db=db)
    return bundle_postings or []

# Endpoint for getting queired bundle postings
# Will return bundle postings related to the search query
@router.get("/search/{query}", response_model=list[BundlePostingPublic])
def get_queried_bundles(query: str, db: SessionDep):
    bundle_postings = bundle_posting_service.get_queried_bundle_postings(query=query, db=db)
    return bundle_postings or []

# Endpoint for getting the current sellers bundle postings
@router.get("/me", response_model = list[BundlePostingPublic])
def get_current_sellers_bundles(current_seller: SellerDep, db: SessionDep):
    return current_seller.postings or []

# Endpoint for getting a specific bundle posting by posting id
@router.get("/{posting_id}", response_model = BundlePostingPublic)
def get_bundle(posting_id: int, db: SessionDep):
    bundle = bundle_posting_service.get_bundle_posting(
        posting_id=posting_id,
        db=db
    )
    if bundle is None:
        raise HTTPException(status_code=404, detail="Bundle not found")
    return bundle

# Endpoint for a seller updating there own bundle posting
@router.patch("/{posting_id}", response_model=BundlePostingPublic)
def update_bundle(posting_id: int, bundle_update: BundlePostingUpdate, current_user: SellerDep, db: SessionDep):
    return bundle_posting_service.update_bundle_posting(posting_id=posting_id, bundle_update=bundle_update, db=db, user_id=current_user.user_id)

# Endpoint for an admin updating a bundle posting
@router.patch("/admin/{posting_id}", response_model=BundlePostingPublic)
def admin_update_bundle(posting_id: int, bundle_update: BundlePostingAdminUpdate, current_user: AdminDep, db: SessionDep):
    return bundle_posting_service.update_bundle_posting(posting_id=posting_id, bundle_update=bundle_update, db=db)

# Endpoint for admins to set a bundles status to be deleted
# This does not remove it from the DB but it is not returned by get active bundles
@router.delete("/delete/{posting_id}", response_model=BundlePostingPublic)
def set_bundle_deleted(posting_id: int, current_user: AdminDep, db: SessionDep):
    return bundle_posting_service.set_bundle_deleted(posting_id=posting_id, db=db)

# Endpoint for the current seller to set there own bundle deleted
@router.delete("/me/{posting_id}")
def set_current_sellers_bundle_deleted(posting_id: int, current_user: SellerDep, db: SessionDep):
    posting = bundle_posting_service.get_bundle_posting(posting_id=posting_id, db=db)
    if posting in current_user.postings:
        bundle_posting_service.set_bundle_deleted(posting_id=posting_id, db=db)
    else:
        raise HTTPException(status_code=403, detail="Current seller does not own this bundle")

# Endpoint for deleting a specific bundle
@router.delete("/{posting_id}")
def delete_bundle(posting_id: int, current_user: AdminDep, db: SessionDep):
    bundle_posting_service.delete_bundle_posting(posting_id=posting_id, db=db)