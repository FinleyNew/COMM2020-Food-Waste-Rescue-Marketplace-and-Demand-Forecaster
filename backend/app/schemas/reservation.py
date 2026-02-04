from sqlmodel import SQLModel

class ReservationBase(SQLModel):
    posting_id: int
    user_id: int
    timestamp: int

class ReservationCreate(ReservationBase):
    pass

class ReservationPublic(ReservationBase):
    claim_code: str
    status: str