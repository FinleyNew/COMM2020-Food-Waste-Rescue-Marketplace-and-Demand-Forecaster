from sqlmodel import Session, select, col, func, extract, Time
from typing import Sequence
from datetime import datetime
from app.models.enums import Category
from app.models import Record

def get_all_records(db: Session) -> Sequence[Record]:
    statement = select(Record)
    return db.exec(statement).all()

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
