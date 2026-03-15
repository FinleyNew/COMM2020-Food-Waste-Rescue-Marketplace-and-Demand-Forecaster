from fastapi import HTTPException
from sqlmodel import Session
from typing import Sequence
from app.models.bundlePosting import BundlePosting
from app.schemas.bundlePosting import BundlePostingAdminUpdate, BundlePostingCreate, BundlePostingUpdate
from app.crud import bundlePosting as bundlePosting_crud
from app.services import reservation as reservation_service
from app.services import forecast as forecast_service
from psycopg2.extras import DateTimeRange
from psycopg.types.range import Range

# The service for creating bundle postings
def create_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, db: Session) -> BundlePosting:
    # Creates the pickup range from the start and end time
    pickup_range = f"[{bundle_in.start_time.isoformat()}, {bundle_in.end_time.isoformat()})"
    bundle_posting = bundlePosting_crud.create_bundle_posting(bundle_in = bundle_in, owner_id=owner_id, pickup_window=pickup_range, db=db)
    forecast_service.create_forecast(bundle_in=bundle_in, posting_id=bundle_posting.posting_id, db=db)
    return bundle_posting

# The service for getting all available bundle postings
def get_active_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_active_bundle_postings(db=db)

def get_queried_bundle_postings(query: str, db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_queried_bundle_postings(query=query, db=db)

# The service for getting all bundles
def get_all_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_all_bundle_postings(db=db)

# The sertvice for getting a specific bundle posting
def get_bundle_posting(posting_id: int, db: Session, lock: bool = False) -> BundlePosting:
    return bundlePosting_crud.get_bundle_posting(posting_id=posting_id, db=db, lock=lock)

# The service for getting a sellers postings
def get_bundle_postings_by_owner(owner_id: int, db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_bundle_postings_by_owner(owner_id = owner_id, db=db)

# The service for consumers to reserve a bundle
def reserve_bundle_posting(posting_id: int, db: Session):
    bundlePosting_crud.reserve_bundle_posting(posting_id=posting_id, db=db)

def update_bundle_posting(posting_id: int, bundle_update: BundlePostingUpdate | BundlePostingAdminUpdate, db: Session, user_id: int | None = None) -> BundlePosting:
    db_bundle = bundlePosting_crud.get_bundle_posting(posting_id=posting_id, db=db, lock=False)

    # If a user_id is provided ensure it matches the owner
    if user_id is not None and db_bundle.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorised to update this posting")

    # Ensures that the pickup window is still valid
    new_start = bundle_update.start_time if bundle_update.start_time is not None else db_bundle.pickup_window.lower
    new_end = bundle_update.end_time if bundle_update.end_time is not None else db_bundle.pickup_window.upper
    if new_end <= new_start:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
    pickup_range = f"[{new_start.isoformat()}, {new_end.isoformat()})"
    
    return bundlePosting_crud.update_bundle_posting(db_bundle=db_bundle, bundle_update=bundle_update, pickup_window=pickup_range, db=db)

def set_bundle_deleted(posting_id: int, db: Session) -> BundlePosting:
    bundle = get_bundle_posting(posting_id=posting_id, db=db)
    for reservation in bundle.reservations:
        reservation_service.delete_reservation(reservation_id=reservation.reservation_id, db=db) # type: ignore
    return bundlePosting_crud.set_bundle_deleted(bundle=bundle, db=db)

# The service for deleting a bundle posting
# Currently not in use
def delete_bundle_posting(posting_id: int, db: Session):
    bundle_posting = get_bundle_posting(posting_id=posting_id, db=db)
    for reservation in bundle_posting.reservations:
        reservation_service.delete_reservation(reservation_id=reservation.reservation_id, db=db) # type: ignore
    bundlePosting_crud.delete_bundle_posting(posting_id=posting_id, db=db)