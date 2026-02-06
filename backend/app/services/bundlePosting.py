from sqlmodel import Session
from app.models.bundlePosting import BundlePosting
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud.bundlePosting import create_bundle_posting, get_all_bundle_postings, get_bundle_posting, is_available

def create_new_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, db: Session) -> BundlePosting:
    return create_bundle_posting(bundle_in = bundle_in, owner_id=owner_id, db=db)

def get_active_bundle_postings(db: Session) -> list[BundlePosting]:
    return get_all_bundle_postings(db=db)

def get_bundle_posting(bundle_id: int, db: Session) -> BundlePosting:
    return get_bundle_posting(bundle_id=bundle_id, db=db)

def is_available(bundle_id: int, db: Session) -> bool:
    return is_available(bundle_id=bundle_id, db=db)