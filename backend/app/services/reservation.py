from sqlmodel import Session
from fastapi import HTTPException
from typing import Sequence
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from app.crud import reservation as reservation_crud
from app.services.bundlePosting import get_bundle_posting, reserve_bundle_posting
from app.models.enums import ReservationStatus

def create_reservation(reservation_in: ReservationCreate, consumer_id: int, posting_id: int, db: Session) -> Reservation:
    bundle = get_bundle_posting(posting_id=posting_id, db=db, lock=True)

    if bundle.available <= 0:
        raise ValueError("No bundles left")
    
    new_reservation = reservation_crud.create_reservation(reservation_in, consumer_id=consumer_id, db=db)
    
    reserve_bundle_posting(posting_id=posting_id, db=db)

    db.commit()
    db.refresh(new_reservation)
    return new_reservation
    
def collect_by_code(claim_code: str, db: Session) -> Reservation:
    reservation = reservation_crud.get_reservation_by_claim_code(claim_code=claim_code, db=db)
    if not reservation:
        raise HTTPException(status_code = 404, detail = "No reservation with that code")
    reservation.status = ReservationStatus.COLLECTED
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

def delete_reservation(reservation_id: int, db: Session):
    reservation_crud.delete_reservation(reservation_id=reservation_id, db=db)

def get_no_show(posting_id: int, db: Session) -> int:
    no_show_count = 0
    reservations: Sequence[Reservation] = reservation_crud.get_reservations_by_posting(posting_id=posting_id, db=db)
    for reservation in reservations:
        if reservation.status == "":
            no_show_count += 1
    return no_show_count