from datetime import datetime
from sqlmodel import SQLModel
from app.models.enums import ReservationStatus

# The base schema for reservations
class ReservationBase(SQLModel):
    posting_id: int
    user_id: int

# The create schema for reservations
class ReservationCreate(ReservationBase):
    pass

# The public schema for reservations
class ReservationPublic(ReservationBase):
    reservation_id: int
    claim_code: str
    status: ReservationStatus
    timestamp: datetime