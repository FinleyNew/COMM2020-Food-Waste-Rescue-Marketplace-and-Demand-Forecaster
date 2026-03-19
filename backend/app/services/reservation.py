from sqlmodel import Session
from fastapi import HTTPException
from typing import Sequence
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationAdminUpdate, ReservationCreate
from app.crud import reservation as reservation_crud
from app.services.bundlePosting import get_bundle_posting, reserve_bundle_posting
from app.models.enums import ReservationStatus

def get_all_reservations(db: Session) -> Sequence[Reservation]:
    return reservation_crud.get_all_reservations(db=db)

# The service for creating a reservation
def create_reservation(reservation_in: ReservationCreate, consumer_id: int, posting_id: int, db: Session) -> Reservation:
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
    return new_reservation

def update_reservation(reservation_id: int, reservation_update: ReservationAdminUpdate, db: Session) -> Reservation:
    db_reservation = reservation_crud.get_reservation_by_id(reservation_id=reservation_id, db=db)
    return reservation_crud.update_reservation(db_reservation=db_reservation, reservation_update=reservation_update, db=db)
    
# The service function for collecting a reservation by code
def collect_by_code(claim_code: str, db: Session) -> Reservation:
    reservation = reservation_crud.get_reservation_by_claim_code(claim_code=claim_code, db=db)
    if not reservation:
        raise HTTPException(status_code = 404, detail = "No reservation with that code")
    reservation.status = ReservationStatus.COLLECTED
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

# The service function for deleting a reservation
# Currently not in use
def delete_reservation(reservation_id: int, db: Session):
    reservation_crud.delete_reservation(reservation_id=reservation_id, db=db)