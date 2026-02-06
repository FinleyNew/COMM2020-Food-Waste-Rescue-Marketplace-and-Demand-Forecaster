from fastapi import APIRouter
from app.api.deps import SellerDep, ConsumerDep, SessionDep
from app.schemas.reservation import ReservationCreate, ReservationPublic

router = APIRouter()

@router.post("/", response_model= ReservationPublic)
def create_reservation(reservation_in: ReservationCreate, current_consumer: ConsumerDep, db: SessionDep):
    #Call create reservation service

@router.get("/collect/{collection_code}", response_model= ReservationPublic)
def collect_by_code(collection_code: str, current_seller: SellerDep, db: SessionDep):
    #Call collect by code service
    
@router.get("/me", response_model= list[ReservationPublic])
def get_current_consumers_reservations(current_consumer: ConsumerDep, db: SessionDep):
    # return current_consumer.reservations
    
@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: SessionDep):
    # Call delete reservation service