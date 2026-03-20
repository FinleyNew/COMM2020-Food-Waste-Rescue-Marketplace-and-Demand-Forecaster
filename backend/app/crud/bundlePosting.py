from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlmodel import Session, select, or_
from typing import Sequence, Tuple
from app.models import BundlePosting, Seller
from app.schemas.bundlePosting import BundlePostingCreate, BundlePostingUpdate
from app.models.enums import BundleStatus, Category
from psycopg.types.range import Range
from app.models.enums import BundleStatus
from sqlalchemy import func

# The crud function for creating a new bundle posting
def create_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, pickup_window: str, db: Session) -> BundlePosting:
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

def get_to_be_expired_bundle_postings(now: datetime, db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting).where(func.upper(BundlePosting.pickup_window) <= now).where(BundlePosting.status.in_([BundleStatus.AVAILABLE, BundleStatus.SOLD_OUT])) # type: ignore
    return db.exec(statement).all()

def get_queried_bundle_postings(query: str, db: Session) -> Sequence[BundlePosting]:
    search = f"%{query}%"  # % is SQL wildcard
    matching_categories = [
    c for c in Category 
    if query.lower() in c.value.lower() or c.value.lower() in query.lower()]
    statement = select(BundlePosting).join(Seller).where(or_(BundlePosting.category.in_(matching_categories), Seller.name.ilike(search))).where(BundlePosting.status == BundleStatus.AVAILABLE) # type: ignore
    return db.exec(statement).all()

def get_to_be_emailed_bundle_postings(now: datetime, db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting).where(func.lower(BundlePosting.pickup_window) - timedelta(minutes=30) <= now).where(func.lower(BundlePosting.pickup_window) - timedelta(minutes=29) > now)
    return db.exec(statement).all()

def set_expired(bundle_posting: BundlePosting, db: Session):
    bundle_posting.status = BundleStatus.EXPIRED

# The crud function for getting a specific bundle posting
def get_bundle_posting(posting_id: int, db: Session, lock: bool) -> BundlePosting:
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    # lock is used when getting ensuring the bundle is available
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

def update_bundle_posting(db_bundle: BundlePosting, bundle_update: BundlePostingUpdate, pickup_window: str | None, db: Session) -> BundlePosting:
    update_data = bundle_update.model_dump(exclude_unset=True, exclude={"start_time", "end_time"})
    db_bundle.sqlmodel_update(update_data)
    if pickup_window:
        db_bundle.pickup_window = pickup_window
    db.commit()
    db.refresh(db_bundle)
    return db_bundle

def set_bundle_deleted(bundle: BundlePosting, db: Session) -> BundlePosting:
    bundle.status = BundleStatus.DELETED
    db.commit()
    db.refresh(bundle)
    return bundle

# The crud function for deleting a bundle posting
# Currently not in use
def delete_bundle_posting(posting_id: int, db: Session):
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    bundle_posting = db.exec(statement).first()

    if bundle_posting:
        db.delete(bundle_posting)
        db.commit()