import httpx
from sqlmodel import Session, select, col, func, extract, Time
from typing import Sequence
from datetime import datetime
from app.models.enums import Category
from app.models import Record
from app.schemas.record import RecordAdminUpdate
from app.models.bundlePosting import BundlePosting
from app.core.config import settings
from app.models.reservation import Reservation
from app.crud import reservation as reservation_crud

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

def create_record(bundle_posting: BundlePosting, latitude: float | None, longitude: float | None, db: Session) -> Record:
    posting_id = BundlePosting.posting_id
    if not posting_id:
        raise Exception("Posting does not exist")
    record = Record.model_validate(
        bundle_posting,
        update={
            "raining": is_raining(latitude=latitude, longitude=longitude),
            "observed_reservations": bundle_posting.reserved,
            "observed_no_show": get_no_show(posting_id=posting_id, db=db),
            "observed_expired": bundle_posting.available
        }
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

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

# The service function for getting the number of no shows for a specific posting
# Used when creating a record
def get_no_show(posting_id: int, db: Session) -> int:
    no_show_count = 0
    reservations: Sequence[Reservation] = reservation_crud.get_reservations_by_posting(posting_id=posting_id, db=db)
    for reservation in reservations:
        if reservation.status == "":
            no_show_count += 1
    return no_show_count


def is_raining(latitude: float | None, longitude: float | None) -> bool:
    # If no coordinates are set assume no rain
    if not latitude:
        return False
    with httpx.Client() as client:
        response = client.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": settings.OPENWEATHER_API_KEY
            }
        )
        data = response.json()
        weather_id = data["weather"][0]["id"]
        return 500 <= weather_id <= 531