from datetime import datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import Column
from sqlmodel import Field, SQLModel
from pydantic import computed_field, model_validator

from app.models.enums import Category, BundleStatus

# The base schema for bundle postings
class BundlePostingBase(SQLModel):
    user_id: int
    category: Category
    allergens: str
    # Can't have a negative ammount of bundles
    available: int = Field(ge=0) 
    # Price should only have 2 decimal places
    price: Decimal = Field(ge=0, decimal_places=2) 
    # Weight is in grams
    weight: int = Field(gt=0) 
    
# The create schema for bundle postings
# Inherits from base 
class BundlePostingCreate(BundlePostingBase):
    start_time: datetime
    end_time: datetime
    # When creating available has to be greater than 0
    available: int = Field(gt=0)
    # Ensures that the start_time comes afer the end_time
    @model_validator(mode="after")
    def check_end_after_start(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self
    
class BundlePostingUpdate(SQLModel):
    category: Category | None = None
    allergens: str | None = None
    available: int | None = Field(default=None, ge=0)
    price: Decimal | None = Field(default=None, ge=0, decimal_places=2)
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
    
class BundlePostingAdminUpdate(BundlePostingUpdate):
    user_id: int | None = None
    status: BundleStatus | None = None

# The public schema for bundle postings
# Inherits from base 
class BundlePostingPublic(BundlePostingBase):
    posting_id: int
    reserved: int = Field(ge=0)
    status: BundleStatus
    pickup_window: Any = Field(exclude=True)

    # This is a coputed field to return the price as a string
    @computed_field
    def price_display(self) -> str:
        return f"{self.price:.2f}"
    
    #This gets the data of the pickup in the form DD/MM/YYYY
    @computed_field
    def formatted_date(self) -> str:
        return self.pickup_window.lower.strftime("%d/%m/%Y")
    
    #This gets the time range in the form HH:MM
    @computed_field
    def formatted_time_range(self) -> str:
        start: datetime = self.pickup_window.lower
        end: datetime = self.pickup_window.upper
        return f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"
    
    model_config = {"from_attributes": True}