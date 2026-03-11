from sqlmodel import Session
from typing import Sequence
from datetime import datetime, timezone
from app.models.record import Record
from app.models.bundlePosting import BundlePosting
from app.schemas.record import RecordCreate
from app.crud import record as record_crud

# The service function for creating a record
# Not currently in use
def create_record(bundle_posting: BundlePosting, db: Session) -> Record:
    posting_id = BundlePosting.posting_id
    if not posting_id:
        raise Exception("Posting does not exist")
    return record_crud.create_record(bundle_posting=bundle_posting, posting_id=posting_id, db=db)