from sqlmodel import Session
from typing import Sequence
from datetime import datetime, timezone
from app.models.record import Record
from app.models.bundlePosting import BundlePosting
from app.schemas.record import RecordCreate
from app.crud import record as record_crud
from app.services.reservation import get_no_show
from random import randint

# The service function for creating a record
# Not currently in use
def create_record(bundle_posting: BundlePosting, db: Session) -> Record:
    posting_id = BundlePosting.posting_id
    if not posting_id:
        raise Exception("Posting does not exist")
    record = Record.model_validate(
        bundle_posting,
        update={
            "raining": is_raining(),
            "observed_reservations": bundle_posting.reserved,
            "observed_no_show": get_no_show(posting_id=posting_id, db=db)
        }
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

# Will just have a 1 in 10 chance of rain for any record
def is_raining():
    rnd = randint(0,9)
    if rnd == 0:
        return True
    else:
        return False