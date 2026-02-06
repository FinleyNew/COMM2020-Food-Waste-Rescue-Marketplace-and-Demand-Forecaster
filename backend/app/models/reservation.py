from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .consumer import Consumer
    from .bundlePosting import BundlePosting

class Reservation(SQLModel, table=True):
    reservation_id: Optional[int] = Field(default=None, primary_key=True)
    posting_id: Optional[int] = Field(default=None, foreign_key="bundleposting.posting_id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    timestamp: str
    claim_code: str
    status: str

    consumer: "Consumer" = Relationship(back_populates="reservation")
    posting: "BundlePosting" = Relationship(back_populates="reservation")