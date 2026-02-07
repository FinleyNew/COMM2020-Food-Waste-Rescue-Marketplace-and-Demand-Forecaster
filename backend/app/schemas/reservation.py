from datetime import datetime
from sqlmodel import SQLModel
from models.enums import ReservationStatus

class ReservationBase(SQLModel):
    posting_id: int
    user_id: int
    timestamp: datetime

class ReservationCreate(ReservationBase):
    pass

class ReservationPublic(ReservationBase):
    reservation_id: int
    claim_code: str
    status: ReservationStatus