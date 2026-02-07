from sqlmodel import Session
from typing import Sequence
import secrets
import string
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from app.crud import reservation as reservation_crud
from app.services.bundlePosting import get_bundle_posting, bundle_reserved

def create_reservation_service(reservation_in: ReservationCreate, consumer_id: int, posting_id: int, db: Session) -> Reservation:
    bundle = get_bundle_posting(posting_id=posting_id, db=db, lock=True)

    if bundle.available <= 0:
        raise ValueError("No bundles left")
    
    new_reservation = reservation_crud.create_reservation(reservation_in, consumer_id=consumer_id, db=db)
    
    bundle_reserved(posting_id=posting_id, db=db)

    db.commit()
    db.refresh(new_reservation)
    return new_reservation
    

def get_reservation_by_claim_code(claim_code: str, seller_id: int, db: Session) -> Reservation:
    return reservation_crud.get_reservation_by_code(claim_code=claim_code, seller_id=seller_id, db=db)
    
def collect_by_code(claim_code: str):