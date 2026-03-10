from datetime import datetime

from pydantic import field_validator
from sqlmodel import Field, SQLModel

# The base schema for sellers
class SellerBase(SQLModel):
    name: str
    location: str
    open_hours: str
    # Ensures open_hours is in the right format and valid
    @field_validator("open_hours")
    @classmethod
    def validate_open_hours(cls, v):
        try:
            open_str, close_str = v.split(" - ")
            open_time = datetime.strptime(open_str, "%H:%M")
            close_time = datetime.strptime(close_str, "%H:%M")
        except ValueError:
            raise ValueError("open_hours must be in the format HH:MM - HH:MM")
        if close_time <= open_time:
            raise ValueError("Closing time must be after opening time")
        return v

#No create schema as we cannot create users yet

# The public schema for seller
class SellerPublic(SellerBase):
    user_id: int

# Summary of seller info that is returned with a bundle
class SellerSummary(SQLModel):
    name: str