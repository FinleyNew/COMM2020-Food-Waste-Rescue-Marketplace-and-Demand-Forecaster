from datetime import datetime
from sqlmodel import SQLModel
from app.models.enums import ReservationStatus

class ReservationBase(SQLModel):
    posting_id: int
    user_id: int

class ReservationCreate(ReservationBase):
    pass

class ReservationPublic(ReservationBase):
    reservation_id: int
    claim_code: str
    status: ReservationStatus
    timestamp: datetime