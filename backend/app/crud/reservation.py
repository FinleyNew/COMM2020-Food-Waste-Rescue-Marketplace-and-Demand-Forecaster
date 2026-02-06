from sqlmodel import Session, select
from typing import Sequence
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate

def create_reservation(reservation_in: ReservationCreate, consumer_id: int, db: Session):
    db_reservation = Reservation.model_validate(reservation_in, update={"consumer_id": consumer_id})
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservations_by_consumer(consumer_id: int, db: Session) -> Sequence[Reservation]:
    statement = select(Reservation).where(Reservation.user_id == consumer_id)
    return db.exec(statement).all()

def get_reservation_by_code(claim_code: str, seller_id, db: Session) -> Reservation:
    statement = select(Reservation).where(Reservation.claim_code == claim_code).where(Reservation.user_id == seller_id)
    return db.exec(statement).one()

def reservation_collected(reservation: Reservation, db: Session):
    reservation.status = #Collected?
    db.add(reservation)
    db.commit()

def delete_reservation(reservation_id: int, db: Session):
    statement = select(Reservation).where(Reservation.reservation_id == reservation_id)
    reservation = db.exec(statement).first()

    if reservation:
        db.delete(reservation)
        db.commit()