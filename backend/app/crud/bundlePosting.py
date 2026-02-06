from sqlmodel import Session, select
from typing import Sequence
from app.models.bundlePosting import BundlePosting
from app.schemas.bundlePosting import BundlePostingCreate, BundlePostingPublic

def create_bundle_posting(bundle_in: BundlePostingCreate, owner_id: int, db: Session) -> BundlePosting:
    #Convert the Schema into a Model
    db_bundle_posting = BundlePosting.model_validate(bundle_in, update={"owner_id": owner_id})
    db.add(db_bundle_posting)
    db.commit()
    db.refresh(db_bundle_posting)
    return db_bundle_posting

def get_all_bundle_postings(db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting)
    return db.exec(statement).all()

def get_posting(posting_id: int, db: Session) -> BundlePosting:
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    return db.exec(statement).one()

def get_postings_by_owner(owner_id: int, db: Session) -> Sequence[BundlePosting]:
    statement = select(BundlePosting).where(BundlePosting.user_id == owner_id)
    return db.exec(statement).all()

def is_available(posting_id: int, db: Session) -> bool:
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    bundle_posting = db.exec(statement).one()

    return (bundle_posting.available != 0)

def delete_posting(posting_id: int, db: Session):
    statement = select(BundlePosting).where(BundlePosting.posting_id == posting_id)
    bundle_posting = db.exec(statement).first()

    if bundle_posting:
        db.delete(bundle_posting)
        db.commit()