from fastapi import HTTPException
from sqlmodel import Session
from typing import Sequence
from datetime import datetime, timezone
from app.models.record import Record
from app.models.bundlePosting import BundlePosting
from app.schemas.record import RecordAdminUpdate, RecordCreate
from app.crud import record as record_crud
from random import randint

def get_all_records(db: Session) -> Sequence[Record]:
    return record_crud.get_all_records(db=db)

def update_record(record_id: int, record_update: RecordAdminUpdate, db: Session) -> Record:
    db_record = record_crud.get_record_by_id(record_id=record_id, db=db)
    # Ensures that the pickup window is still valid
    new_start = record_update.start_time if record_update.start_time is not None else db_record.pickup_window.lower
    new_end = record_update.end_time if record_update.end_time is not None else db_record.pickup_window.upper
    if new_end <= new_start:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
    pickup_range = f"[{new_start.isoformat()}, {new_end.isoformat()})"

    return record_crud.update_record(db_record=db_record, record_update=record_update, pickup_window=pickup_range, db=db)

# The service function for creating a record
# Not currently in use
def create_record(bundle_posting: BundlePosting, db: Session) -> Record:
    latitude = bundle_posting.seller.latitude
    longitude = bundle_posting.seller.longitude
    return record_crud.create_record(bundle_posting=bundle_posting, latitude=latitude, longitude=longitude, db=db)


    
def delete_record(record_id: int, db: Session):
    record_crud.delete_record(record_id=record_id, db=db)
