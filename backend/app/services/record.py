from sqlmodel import Session
from typing import Sequence
from datetime import datetime, timezone
from app.models.record import Record
from app.models.bundlePosting import BundlePosting
from app.schemas.record import RecordCreate
from app.crud import record as record_crud

def create_record(bundle_posting: BundlePosting, db: Session) -> Record:
    record = Record.model_validate(
        bundle_posting,
        update={
            "raining":,
            "observed_reservations": bundle_posting.reserved,
            "observed_no_show"
        }
    )

