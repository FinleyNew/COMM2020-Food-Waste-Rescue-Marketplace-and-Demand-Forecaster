from datetime import datetime
from decimal import Decimal
from typing import Any
from sqlalchemy import Column
from sqlmodel import Field, SQLModel
from pydantic import computed_field

from models.enums import Category, BundleStatus

class BundlePostingBase(SQLModel):
    user_id: int
    category: Category
    allergens: str
    available: int
    price: Decimal
    

class BundlePostingCreate(BundlePostingBase):
    start_time: datetime
    end_time: datetime

class BundlePostingPublic(BundlePostingBase):
    posting_id: int
    reserved: int
    status: BundleStatus
    pickup_window: Any = Field(exclude=True)

    @computed_field
    def price_display(self) -> str:
        return f"{self.price:.2f}"
    
    @computed_field
    def start_time(self) -> datetime:
        #automatically pulls from the db_bundle.pickup_window.lower
        return self.pickup_window.lower
    
    @computed_field
    def end_time(self) -> datetime:
        return self.pickup_window.upper
    
    model_config = {"from_attributes": True}