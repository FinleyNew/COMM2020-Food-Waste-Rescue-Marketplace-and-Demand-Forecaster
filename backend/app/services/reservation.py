from sqlmodel import Session
from fastapi import HTTPException
from typing import Sequence
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationAdminUpdate, ReservationCreate
from app.crud import reservation as reservation_crud
from app.services.bundlePosting import get_bundle_posting, reserve_bundle_posting
from app.models.enums import ReservationStatus

# Gets all reservations
def get_all_reservations(db: Session) -> Sequence[Reservation]:
    return reservation_crud.get_all_reservations(db=db)

# The service for creating a reservation
def create_reservation(reservation_in: ReservationCreate, consumer_id: int, posting_id: int, db: Session) -> Reservation:
    from app.services.badge import check_at_reservation
    # this gets the corresponding bundle from the DB and locks it so no other service can access it
    bundle = get_bundle_posting(posting_id=posting_id, db=db, lock=True)
    # It then checks if any bundles are left
    if bundle.available <= 0:
        raise ValueError("No bundles left")
    # If there are create a new reservation
    new_reservation = reservation_crud.create_reservation(reservation_in, consumer_id=consumer_id, db=db)
    
    reserve_bundle_posting(posting_id=posting_id, db=db)
    db.commit()
    db.refresh(new_reservation)
    check_at_reservation(consumer_id=consumer_id, db=db)

    return new_reservation

# Updates a reservation
def update_reservation(reservation_id: int, reservation_update: ReservationAdminUpdate, db: Session) -> Reservation:
    db_reservation = reservation_crud.get_reservation_by_id(reservation_id=reservation_id, db=db)
    return reservation_crud.update_reservation(db_reservation=db_reservation, reservation_update=reservation_update, db=db)
    
# The service function for collecting a reservation by code
def collect_by_code(claim_code: str, db: Session) -> Reservation:
    from app.services.badge import check_at_collection
    reservation = reservation_crud.get_reservation_by_claim_code(claim_code=claim_code, db=db)
    # Ensures this claim code links to a reservation
    if not reservation:
        raise HTTPException(status_code = 404, detail = "No reservation with that code")
    # Ensures this reservation hasn't already been collected
    elif reservation.status == ReservationStatus.COLLECTED:
        raise HTTPException(status_code = 400, detail = "Reservation has already been collected")
    # Ensures this reservation hasn't already expired
    elif reservation.status == ReservationStatus.NO_SHOW:
        raise HTTPException(status_code = 400, detail = "Reservation was marked as no-show and cannot be collected")
    reservation.status = ReservationStatus.COLLECTED
    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    check_at_collection(consumer_id=reservation.user_id, db=db) # type: ignore

    return reservation

# The service function for deleting a reservation
def delete_reservation(reservation_id: int, db: Session):
    reservation_crud.delete_reservation(reservation_id=reservation_id, db=db)