from datetime import datetime
from sqlmodel import Session, select
from typing import Sequence, Tuple
from app.models import BundlePosting
from app.schemas.bundlePosting import BundlePostingCreate
from psycopg.types.range import Range

def create_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, pickup_window, db: Session) -> BundlePosting:
    #Convert the Schema into a Model
    db_bundle_posting = BundlePosting.model_validate(bundle_in, update={"owner_id": owner_id, "pickup_window": pickup_window})
    db.add(db_bundle_posting)
    db.commit()
    db.refresh(db_bundle_posting)
    return db_bundle_posting

def get_active_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting)
    return db.exec(statement).all()

def get_bundle_posting(posting_id: int, db: Session, lock: bool) -> BundlePosting:
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    if lock:
        statement = statement.with_for_update()
    return db.exec(statement).one()

def get_bundle_postings_by_owner(owner_id: int, db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting).where(BundlePosting.user_id == owner_id)
    return db.exec(statement).all()

# def is_available(posting_id: int, db: Session) -> bool:
#     statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
#     bundle_posting = db.exec(statement).one()

#     return (bundle_posting.available != 0)

def reserve_bundle_posting(posting_id: int, db: Session):
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    bundle_posting = db.exec(statement).one()

    bundle_posting.available -= 1
    bundle_posting.reserved += 1

    db.add(bundle_posting)

def delete_bundle_posting(posting_id: int, db: Session):
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    bundle_posting = db.exec(statement).first()

    if bundle_posting:
        db.delete(bundle_posting)
        db.commit()