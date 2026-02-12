from sqlmodel import Session
from typing import Sequence
from app.models.bundlePosting import BundlePosting
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud import bundlePosting as bundlePosting_crud
from psycopg2.extras import DateTimeRange
from psycopg.types.range import Range

def create_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, db: Session) -> BundlePosting:
    pickup_range = f"[{bundle_in.start_time.isoformat()}, {bundle_in.end_time.isoformat()})"
    #Here it will call the create forecast method
    return bundlePosting_crud.create_bundle_posting(bundle_in = bundle_in, owner_id=owner_id, pickup_window=pickup_range, db=db)

def get_active_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_active_bundle_postings(db=db)

def get_bundle_posting(posting_id: int, db: Session, lock: bool = False) -> BundlePosting:
    return bundlePosting_crud.get_bundle_posting(posting_id=posting_id, db=db, lock=lock)

def get_bundle_postings_by_owner(owner_id: int, db: Session) -> Sequence[BundlePosting]:
    return bundlePosting_crud.get_bundle_postings_by_owner(owner_id = owner_id, db=db)

def reserve_bundle_posting(posting_id: int, db: Session):
    bundlePosting_crud.reserve_bundle_posting(posting_id=posting_id, db=db)

def delete_bundle_posting(posting_id: int, db: Session):
    #Should generate a record here
    #You want to fetch the corresponding posting
    bundle_posting = get_bundle_posting(posting_id=posting_id, db=db)
    #Call create record service (New Id and other aditional attributes)

    bundlePosting_crud.delete_bundle_posting(posting_id=posting_id, db=db)