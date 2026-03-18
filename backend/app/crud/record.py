from sqlmodel import Session, select, col, func, extract, Time
from typing import Sequence
from datetime import datetime
from app.models.enums import Category
from app.models import Record
from app.schemas.record import RecordAdminUpdate
from app.models.bundlePosting import BundlePosting
from random import randint

from app.services import reservation as reservation_service

def create_record(bundle_posting: BundlePosting, posting_id: int, db: Session) -> Record:
    record = Record.model_validate(
        bundle_posting,
        update={
            "raining": is_raining(),
            "observed_reservations": bundle_posting.reserved,
            "observed_no_show": reservation_service.get_no_show(posting_id=posting_id, db=db),
            "observed_expired": bundle_posting.available
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



def update_record(db_record: Record, record_update: RecordAdminUpdate, pickup_window: str | None, db: Session) -> Record:
    update_data = record_update.model_dump(exclude_unset=True)
    db_record.sqlmodel_update(update_data)
    if pickup_window:
        db_record.pickup_window = pickup_window
    db.commit()
    db.refresh(db_record)
    return db_record

def get_record_by_id(record_id: int, db: Session):
    statement = select(Record).where(Record.record_id == record_id)
    return db.exec(statement).one()

# Crud function for getting all the records from the database
# Is used for training the model
def get_all_records(db: Session) -> Sequence[Record]:
    statement = select(Record)
    return db.exec(statement).all()

# Crud function for getting all records with the same time window and day of week
def get_same_time_records(search_start: Time, search_end: Time, day_of_week: int, db: Session) -> Sequence[Record]:
    statement = (
        select(Record)
        .where(
            func.lower(Record.pickup_window).cast(Time) == search_start,
            func.upper(Record.pickup_window).cast(Time) == search_end
        ).where(
            # 0 is Sunday, 6 is Saturday
            func.extract('dow', func.lower(Record.pickup_window)) == day_of_week
        )
    )
    return db.exec(statement).all()

def delete_record(record_id: int, db: Session):
    statement = select(Record).where(Record.record_id == record_id)
    record = db.exec(statement).first()
    if record:
        db.delete(record)
        db.commit()