from typing import Optional, TYPE_CHECKING, Any
from decimal import Decimal
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, Index
from sqlalchemy.dialects import postgresql
from .enums import Category

if TYPE_CHECKING:
    from .seller import Seller
    from .bundlePosting import BundlePosting


class Record(SQLModel, table=True):
    record_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    posting_id: Optional[int] = Field(default=None, foreign_key="bundleposting.posting_id")
    # day_of_week: int
    # time_window: str
    pickup_window: Any = Field(sa_column=Column(postgresql.TSTZRANGE, index=True))
    category: Category
    price: Decimal = Field(sa_column=Column(postgresql.NUMERIC(precision=10, scale=2)))
    raining: bool
    observed_reservations: int
    observed_no_show: int

    seller: "Seller" = Relationship(back_populates="record")
    posting: "BundlePosting" = Relationship(back_populates="record")