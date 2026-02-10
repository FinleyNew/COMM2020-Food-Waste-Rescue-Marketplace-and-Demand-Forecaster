from typing import Sequence
from fastapi import HTTPException
from datetime import datetime, timezone
from sqlmodel import Session
from datetime import datetime, timezone
from app.crud.reservation import get_reservations_by_consumer
from app.models.reservation import Reservation
from app.crud import consumer as consumer_crud

# def create_consumer():

def check_streak(consumer_id: int, db: Session):
    # Get the latest reservation that the consumer has placed
    reservations: Sequence[Reservation] = get_reservations_by_consumer(consumer_id=consumer_id, db=db)
    if not reservations:
        raise HTTPException(status_code = 404, detail = "No reservations found for this ID")
    # Get the timestamp from that reservation
    reservation = reservations[0]
    timestamp = reservation.timestamp
    # Get the current time
    now = datetime.now(timezone.utc)
    # Compare the two if the difference is greater than 1 week then reset the streak to 0
    time_diff = now - timestamp
    if time_diff.days >= 7:
        # Reset the consumers streak
        consumer_crud.reset_consumers_streak(consumer_id=consumer_id, db=db)