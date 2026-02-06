from sqlmodel import SQLModel

class RecordBase(SQLModel):
    user_id: int
    posting_id: int
    day_of_week: #enum
    time_window: ?
    category: str
    price: ?
    raining: bool
    observed_reservations: int
    observed_no_show: int

class RecordCreate(RecordBase):
    pass

class RecordPublic(RecordBase):
    record_id: int