from sqlmodel import Session, select, col, func, extract, Time
from typing import Sequence
from datetime import datetime
from app.models.enums import Category
from app.models import Record
from app.models.bundlePosting import BundlePosting
from app.services.reservation import get_no_show
from random import randint

def create_record(bundle_posting: BundlePosting, posting_id: int, db: Session) -> Record:
    record = Record.model_validate(
        bundle_posting,
        update={
            "raining": is_raining(),
            "observed_reservations": bundle_posting.reserved,
            "observed_no_show": get_no_show(posting_id=posting_id, db=db),
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
