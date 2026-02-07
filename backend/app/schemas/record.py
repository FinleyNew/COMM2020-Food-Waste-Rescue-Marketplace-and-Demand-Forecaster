from datetime import datetime, date
from decimal import Decimal
from typing import Any
from pydantic import computed_field
from sqlmodel import Field, SQLModel

class RecordBase(SQLModel):
    user_id: int
    posting_id: int
    category: str
    price: Decimal
    raining: bool
    observed_reservations: int
    observed_no_show_prob: float

class RecordCreate(RecordBase):
    start_time: datetime
    end_time: datetime

class RecordPublic(RecordBase):
    record_id: int
    pickup_window: Any = Field(exclude=True)

    @computed_field
    def start_time(self) -> datetime:
        return self.pickup_window.lower
    
    @computed_field
    def end_time(self) -> datetime:
        return self.pickup_window.upper
    
    @computed_field
    def pickup_date(self) -> date:
        return self.pickup_window.lower.date()
    
    @computed_field
    def formatted_date(self) -> str:
        return self.pickup_window.lower.strftime("%A, %b %d")