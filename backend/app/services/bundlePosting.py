from sqlmodel import Session
from typing import Sequence
from app.models.bundlePosting import BundlePosting
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud.bundlePosting import create_bundle_posting, get_all_bundle_postings, get_posting, get_postings_by_owner, reserve_bundle, delete_posting

def create_new_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, db: Session) -> BundlePosting:
    return create_bundle_posting(bundle_in = bundle_in, owner_id=owner_id, db=db)

def get_active_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    return get_all_bundle_postings(db=db)

def get_bundle_posting(posting_id: int, db: Session, lock: bool = False) -> BundlePosting:
    return get_posting(posting_id=posting_id, db=db, lock=lock)

def get_bundle_postings_by_owner(owner_id: int, db: Session) -> Sequence[BundlePosting]:
    return get_postings_by_owner(owner_id = owner_id, db=db)

def bundle_reserved(posting_id: int, db: Session):
    return reserve_bundle(posting_id=posting_id, db=db)

def delete_bundle_posting(posting_id: int, db: Session):
    return delete_posting(posting_id=posting_id, db=db)