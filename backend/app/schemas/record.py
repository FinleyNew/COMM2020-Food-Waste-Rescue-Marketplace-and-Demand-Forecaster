from datetime import datetime, date
from decimal import Decimal
from typing import Any
from pydantic import computed_field
from sqlmodel import Field, SQLModel

# The base schema for Records
class RecordBase(SQLModel):
    user_id: int
    posting_id: int
    category: str
    price: Decimal
    raining: bool
    observed_reservations: int
    observed_no_show: int
    observed_expired: int
    weight: int

# The create schema for records
class RecordCreate(RecordBase):
    start_time: datetime
    end_time: datetime

# The public schema for records
class RecordPublic(RecordBase):
    record_id: int
    pickup_window: Any = Field(exclude=True)

    # Computed field to get the start time
    @computed_field
    def start_time(self) -> datetime:
        return self.pickup_window.lower
    
    # Computed field to get the end time
    @computed_field
    def end_time(self) -> datetime:
        return self.pickup_window.upper
    
    # Computed field to get the date
    @computed_field
    def pickup_date(self) -> date:
        return self.pickup_window.lower.date()
    
    # Computed field to get the formatted date
    # exp: Friday, Feb 13
    @computed_field
    def formatted_date(self) -> str:
        return self.pickup_window.lower.strftime("%A, %b %d")