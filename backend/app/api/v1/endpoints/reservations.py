from fastapi import APIRouter
from app.api.deps import SellerDep, ConsumerDep, SessionDep
from app.schemas.reservation import ReservationCreate, ReservationPublic
from app.services import reservation as reservation_service

router = APIRouter()

@router.post("/", response_model= ReservationPublic)
def create_reservation(reservation_in: ReservationCreate, current_consumer: ConsumerDep, db: SessionDep):
    user_id = current_consumer.user_id
    if user_id:
        return reservation_service.create_reservation_service(
            reservation_in=reservation_in,
            consumer_id=user_id,
            posting_id=reservation_in.posting_id,
            db=db
        )

@router.get("/collect/{claim_code}", response_model= ReservationPublic)
def collect_by_code(claim_code: str, current_seller: SellerDep, db: SessionDep):
    user_id = current_seller.user_id
    if user_id:
        return reservation_service.collect_by_code_service(
            claim_code=claim_code,
            seller_id=user_id,
            db=db
        )
    
@router.get("/me", response_model= list[ReservationPublic])
def get_current_consumers_reservations(current_consumer: ConsumerDep, db: SessionDep):
    return current_consumer.reservations
    
@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: SessionDep):
    reservation_service.delete_reservation_service(reservation_id=reservation_id, db=db)