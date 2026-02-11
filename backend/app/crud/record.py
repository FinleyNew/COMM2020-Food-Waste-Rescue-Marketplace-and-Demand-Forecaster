from sqlmodel import Session, select, col, func, extract
from typing import Sequence
from datetime import datetime
from app.models import Record

def get_records_for_forecast(seller_id: int, db: Session) -> Sequence[Record]:
    current_dow = (datetime.now().weekday() + 1) % 7
    statement = select(Record).where(Record.user_id == seller_id).where(extract('dow', func.lower(Record.pickup_window)) == current_dow)
    return db.exec(statement).all()