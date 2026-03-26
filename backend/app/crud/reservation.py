from app.models.bundlePosting import BundlePosting
from sqlmodel import Session, func, select, col
from typing import Sequence
from sqlalchemy.exc import IntegrityError
from app.models import Reservation
from app.models.reservation import generate_claim_code
from app.schemas.reservation import ReservationCreate
from app.models.enums import ReservationStatus
from app.schemas.reservation import ReservationAdminUpdate, ReservationCreate
from app.crud import category as category_crud

# The crud function for getting all reservations
def get_all_reservations(db: Session) -> Sequence[Reservation]:
    statement = select(Reservation)
    return db.exec(statement).all()

# The crud function for creating a reservation
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

# The crud function for updating a reservation
def update_reservation(db_reservation: Reservation, reservation_update: ReservationAdminUpdate, db: Session) -> Reservation:
    update_data = reservation_update.model_dump(exclude_unset=True)
    db_reservation.sqlmodel_update(update_data)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# The crud function for getting a specific reservation
def get_reservation_by_id(reservation_id: int, db: Session) -> Reservation:
    statement = select(Reservation).where(Reservation.reservation_id == reservation_id)
    return db.exec(statement).one()

# The crud function for getting reservations linked to a specific posting
def get_reservations_by_posting(posting_id: int, db: Session) -> Sequence[Reservation]:
    statement = select(Reservation).where(Reservation.posting_id == posting_id)
    return db.exec(statement).all()

# The crud function for getting reservations by a specific consumer
def get_reservations_by_consumer(consumer_id: int, db: Session) -> Sequence[Reservation]:
    statement = select(Reservation).where(Reservation.user_id == consumer_id).order_by(col(Reservation.timestamp).desc())
    return db.exec(statement).all()

# The crud function for getting a reservation by claim code
def get_reservation_by_claim_code(claim_code: str, db: Session) -> Reservation | None:
    statement = select(Reservation).where(Reservation.claim_code == claim_code)
    return db.exec(statement).first()

# The crud function for getting all the collected reservations for a specific user
def get_consumers_collected_reservations(consumer_id: int, db: Session) -> Sequence[Reservation]:
    statement = select(Reservation).where(Reservation.user_id == consumer_id).where(Reservation.status == ReservationStatus.COLLECTED).order_by(Reservation.timestamp.desc()) # type: ignore
    return db.exec(statement).all()

# This checks if the familiar face badge has been earned
# Needs DB level access to check efficiently
def check_familiar_face(consumer_id: int, db: Session) -> bool:
    result = db.exec(
        select(BundlePosting.user_id)
        .join(Reservation, Reservation.posting_id == BundlePosting.posting_id) # type: ignore
        .where(Reservation.user_id == consumer_id)
        .where(Reservation.status == ReservationStatus.COLLECTED)
        .group_by(BundlePosting.user_id) # type: ignore
        .having(func.count(BundlePosting.user_id) >= 3) # type: ignore
    ).first()

    return result is not None

# This checks if the well rounded badge has been earned
# Needs DB level access to check efficiently
def check_well_rounded(consumer_id: int, db: Session) -> bool:
    result = db.exec(
        select(BundlePosting.category_id)
        .join(Reservation, Reservation.posting_id == BundlePosting.posting_id) # type: ignore
        .where(Reservation.user_id == consumer_id)
        .where(Reservation.status == ReservationStatus.COLLECTED)
        .distinct()
    ).all()
    categories = category_crud.get_all_categories(db=db)
    return len(result) >= len(categories)

def set_no_show(reservation: Reservation, db: Session):
    reservation.status = ReservationStatus.NO_SHOW


# The crud function for deleting a reservation
def delete_reservation(reservation_id: int, db: Session):
    statement = select(Reservation).where(Reservation.reservation_id == reservation_id)
    reservation = db.exec(statement).first()

    if reservation:
        db.delete(reservation)
        db.commit()