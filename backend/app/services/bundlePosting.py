from sqlmodel import Session
from typing import Sequence
from app.models.bundlePosting import BundlePosting
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud import bundlePosting as bundlePosting_crud
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

# The service for getting all bundle postings
def get_active_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_active_bundle_postings(db=db)

# The sertvice for getting a specific bundle posting
def get_bundle_posting(posting_id: int, db: Session, lock: bool = False) -> BundlePosting:
    return bundlePosting_crud.get_bundle_posting(posting_id=posting_id, db=db, lock=lock)

# The service for getting a sellers postings
def get_bundle_postings_by_owner(owner_id: int, db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_bundle_postings_by_owner(owner_id = owner_id, db=db)

# The service for consumers to reserve a bundle
def reserve_bundle_posting(posting_id: int, db: Session):
    bundlePosting_crud.reserve_bundle_posting(posting_id=posting_id, db=db)

# The service for deleting a bundle posting
# Currently not in use
def delete_bundle_posting(posting_id: int, db: Session):
    bundle_posting = get_bundle_posting(posting_id=posting_id, db=db)

    bundlePosting_crud.delete_bundle_posting(posting_id=posting_id, db=db)