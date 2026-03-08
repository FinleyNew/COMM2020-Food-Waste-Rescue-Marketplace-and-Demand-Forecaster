from datetime import datetime
from sqlmodel import Session, select
from typing import Sequence, Tuple
from app.models import BundlePosting
from app.schemas.bundlePosting import BundlePostingCreate
from app.models.enums import BundleStatus
from psycopg.types.range import Range

# The crud function for creating a new bundle posting
def create_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, pickup_window, db: Session) -> BundlePosting:
    # Converts the Schema into a Model
    db_bundle_posting = BundlePosting.model_validate(bundle_in, update={"owner_id": owner_id, "pickup_window": pickup_window})
    db.add(db_bundle_posting)
    db.commit()
    db.refresh(db_bundle_posting)
    return db_bundle_posting

# The crud function for getting all available bundle postings
def get_active_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting).where(BundlePosting.status == BundleStatus.AVAILABLE)
    return db.exec(statement).all()

# The crud function for getting all bundles
def get_all_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting)
    return db.exec(statement).all()

# The crud function for getting a specific bundle posting
def get_bundle_posting(posting_id: int, db: Session, lock: bool) -> BundlePosting:
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    # lock is used when getting ensuring the buncle is available
    # It ensures that the bundle can only be accessed one at a time
    if lock:
        statement = statement.with_for_update()
    return db.exec(statement).one()

# The crud function for getting all bundle postings by owner
def get_bundle_postings_by_owner(owner_id: int, db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting).where(BundlePosting.user_id == owner_id)
    return db.exec(statement).all()

# The crud function for reserving a bundle
# It adds one to reserved and takes one from available
def reserve_bundle_posting(posting_id: int, db: Session):
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    bundle_posting = db.exec(statement).one()

    bundle_posting.available -= 1
    bundle_posting.reserved += 1

    db.add(bundle_posting)

# The crud function for deleting a bundle posting
# Currently not in use
def delete_bundle_posting(posting_id: int, db: Session):
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    bundle_posting = db.exec(statement).first()

    if bundle_posting:
        db.delete(bundle_posting)
        db.commit()