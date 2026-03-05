from typing import Sequence
from fastapi import HTTPException
from datetime import datetime, timezone, date, timedelta
from sqlmodel import Session
from app.crud.reservation import get_reservations_by_consumer
from app.models.reservation import Reservation
from app.crud import consumer as consumer_crud

def get_week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())

# Service for checking whether a consumers streak is still valid
def check_streak(consumer_id: int, db: Session) -> bool:
    # Get the latest reservation that the consumer has placed
    reservations: Sequence[Reservation] = get_reservations_by_consumer(consumer_id=consumer_id, db=db)
    if not reservations:
        raise HTTPException(status_code = 404, detail = "No reservations found for this ID")
    # Get the timestamp from that reservation
    reservation = reservations[0]
    timestamp = reservation.timestamp
    # Get the week of the last reservation
    last_reservation_week = get_week_start(timestamp.date())
    # Get the start of the current week
    current_week = get_week_start(date.today())
    # Get the previous week
    previous_week = current_week - timedelta(weeks=1)
    # Check if the week of the last reservation is the current or previous week
    if  not last_reservation_week in (current_week, previous_week):
        # Reset the consumers streak
        consumer_crud.reset_consumers_streak(consumer_id=consumer_id, db=db)
        return False
    return True

def increment_streak(consumer_id: int, streak: int, db: Session):
    #Check the consumers streak to make sure it's still valid
    if streak > 0 and check_streak(consumer_id=consumer_id, db=db):
        #get the consumers latest reservation
        reservations: Sequence[Reservation] = get_reservations_by_consumer(consumer_id=consumer_id, db=db)
        if not reservations:
            raise HTTPException(status_code = 404, detail = "No reservations found for this ID")
        # Get the timestamp from that reservation
        reservation = reservations[0]
        timestamp = reservation.timestamp
        # Get the week of the last reservation
        last_reservation_week = get_week_start(timestamp.date())
        # Get the start of the current week
        current_week = get_week_start(date.today())
        # If the week of the last reservation is the current week don't increment
        if current_week != last_reservation_week:
            consumer_crud.increment_consumers_streak(consumer_id=consumer_id, db=db)
    else:
        consumer_crud.increment_consumers_streak(consumer_id=consumer_id, db=db)