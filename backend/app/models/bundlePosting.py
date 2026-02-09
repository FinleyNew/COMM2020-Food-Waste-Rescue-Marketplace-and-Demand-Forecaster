from datetime import datetime
from typing import Any, Optional, List, TYPE_CHECKING, Tuple
from decimal import Decimal
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from .enums import BundleStatus, Category

if TYPE_CHECKING:
    from .seller import Seller
    from .reservation import Reservation
    from .record import Record
    from .forecast import Forecast


class BundlePosting(SQLModel, table=True):
    posting_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="seller.user_id", index=True)
    category: Category
    allergens: str | None
    available: int
    reserved: int = 0
    price: Decimal = Field(sa_column=Column(postgresql.NUMERIC(precision=10, scale=2)))
    pickup_window: Any = Field(sa_column=Column(postgresql.TSTZRANGE, index=True))
    status: BundleStatus = Field(default=BundleStatus.AVAILABLE)

    seller: "Seller" = Relationship(back_populates="postings")
    reservations: List["Reservation"] = Relationship(back_populates="posting")
    record: "Record" = Relationship(back_populates="posting")
    forecast: "Forecast" = Relationship(back_populates="posting")
