from typing import Optional, TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User
    from.bundlePosting import BundlePosting
    from .record import Record
    from .forecast import Forecast

class Seller(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.user_id")
    name: str
    location: str
    opening_hours: str

    user: "User" = Relationship(back_populates="seller")
    postings: List["BundlePosting"] = Relationship(back_populates="seller")
    records: List["Record"] = Relationship(back_populates="seller")
    forecasts: List["Forecast"] = Relationship(back_populates="seller")