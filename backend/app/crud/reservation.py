from app.models.bundlePosting import BundlePosting
from sqlmodel import Session, select, col
from typing import Sequence
from sqlalchemy.exc import IntegrityError
from app.models import Reservation
from app.models.reservation import generate_claim_code
from app.schemas.reservation import ReservationCreate

# Crud function for creating a reservation
def create_reservation(reservation_in: ReservationCreate, consumer_id: int, db: Session) -> Reservation:
    db_reservation = Reservation.model_validate(reservation_in, update={"consumer_id": consumer_id})
    #Try generating unique claim code five times
    for i in range(5):
        try:
            with db.begin_nested():
                db.add(db_reservation)
                db.flush()
            return db_reservation
        except IntegrityError:
            db_reservation.claim_code = generate_claim_code()
    raise Exception("could not generate unique claim code")

# Crud function for getting reservations linked to a specific posting
def get_reservations_by_posting(posting_id: int, db: Session) -> Sequence[Reservation]:
    statement = select(Reservation).where(Reservation.posting_id == posting_id)
    return db.exec(statement).all()

# Crud function for getting reservations by a specific consumer
def get_reservations_by_consumer(consumer_id: int, db: Session) -> Sequence[Reservation]:
    statement = select(Reservation).where(Reservation.user_id == consumer_id).order_by(col(Reservation.timestamp).desc())
    return db.exec(statement).all()

# Crud function for getting a reservation by claim code
def get_reservation_by_claim_code(claim_code: str, db: Session) -> Reservation | None:
    statement = select(Reservation).where(Reservation.claim_code == claim_code)
    return db.exec(statement).first()

# Crud function for deleting a reservation
# Currently not in use
def delete_reservation(reservation_id: int, db: Session):
    statement = select(Reservation).where(Reservation.reservation_id == reservation_id)
    reservation = db.exec(statement).first()

    if reservation:
        db.delete(reservation)
        db.commit()