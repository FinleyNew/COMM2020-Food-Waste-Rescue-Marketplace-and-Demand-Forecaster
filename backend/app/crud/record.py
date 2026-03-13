from sqlmodel import Session, select, col, func, extract, Time
from typing import Sequence
from datetime import datetime
from app.models.enums import Category
from app.models import Record
from app.schemas.record import RecordAdminUpdate


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