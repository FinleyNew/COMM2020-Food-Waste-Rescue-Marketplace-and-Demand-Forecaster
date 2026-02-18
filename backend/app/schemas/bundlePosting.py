from datetime import datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import Column
from sqlmodel import Field, SQLModel
from pydantic import computed_field

from app.models.enums import Category, BundleStatus

# The base schema for bundle postings
class BundlePostingBase(SQLModel):
    user_id: int
    category: Category
    allergens: str
    available: int
    price: Decimal
    weight: int
    
# The create schema for bundle postings
# Inherits from base 
class BundlePostingCreate(BundlePostingBase):
    start_time: datetime
    end_time: datetime

# The public schema for bundle postings
# Inherits from base 
class BundlePostingPublic(BundlePostingBase):
    posting_id: int
    reserved: int
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