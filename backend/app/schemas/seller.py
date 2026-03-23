from datetime import datetime

from pydantic import field_validator
from sqlmodel import Field, SQLModel

# The base schema for sellers
class SellerBase(SQLModel):
    name: str
    location: str
    opening_hours: str
    logo_url: str

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()
    # Ensures open_hours is in the right format and valid
    @field_validator("opening_hours")
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

class SellerCreate(SellerBase):
    pass

class SellerUpdate(SQLModel):
    name: str | None = None
    location: str | None = None
    opening_hours: str | None = None
    # Ensures open_hours is in the right format and valid
    @field_validator("opening_hours")
    @classmethod
    def validate_open_hours(cls, v):
        if v:
            try:
                open_str, close_str = v.split(" - ")
                open_time = datetime.strptime(open_str, "%H:%M")
                close_time = datetime.strptime(close_str, "%H:%M")
            except ValueError:
                raise ValueError("open_hours must be in the format HH:MM - HH:MM")
            if close_time <= open_time:
                raise ValueError("Closing time must be after opening time")
            return v
        
class SellerAdminUpdate(SellerUpdate):
    pass

# The public schema for seller
class SellerPublic(SellerBase):
    user_id: int

# Summary of seller info that is returned with a bundle
class SellerSummary(SQLModel):
    name: str
    logo_url: str