from datetime import datetime, date
from decimal import Decimal
from typing import Any
from pydantic import computed_field, model_validator
from sqlmodel import Field, SQLModel

from app.schemas.category import CategoryPublic

# The base schema for records
class RecordBase(SQLModel):
    user_id: int
    posting_id: int
    category: CategoryPublic
    # Price should have 2 decimal places and be greater than 0
    price: Decimal = Field(ge=0, decimal_places=2)
    raining: bool
    #These cannot be negative
    observed_reservations: int = Field(ge=0)
    observed_no_show: int = Field(ge=0)
    observed_expired: int = Field(ge=0)
    # Measured in grams, has to be greater than 0
    weight: int = Field(gt=0)

# The create schema for records
class RecordCreate(RecordBase):
    start_time: datetime
    end_time: datetime
    # Ensures that the start_time comes afer the end_time
    @model_validator(mode="after")
    def check_end_after_start(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self
    
# The schema for admins updating a record
class RecordAdminUpdate(SQLModel):
    category: CategoryPublic | None = None
    price: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    raining: bool | None = None
    observed_reservations: int | None = Field(default=None, ge=0)
    observed_no_show: int | None = Field(default=None, ge=0)
    observed_expired: int | None = Field(default=None, ge=0)
    weight: int | None = Field(default=None, gt=0)
    # They could send a new start but not end so need to check in the service
    start_time: datetime | None = None
    end_time: datetime | None = None

    @model_validator(mode="after")
    def check_end_after_start(self):
        # Only validate if both are provided
        if self.start_time is not None and self.end_time is not None:
            if self.end_time <= self.start_time:
                raise ValueError("end_time must be after start_time")
        return self

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
    # ex: Friday, Feb 13
    @computed_field
    def formatted_date(self) -> str:
        return self.pickup_window.lower.strftime("%A, %b %d")