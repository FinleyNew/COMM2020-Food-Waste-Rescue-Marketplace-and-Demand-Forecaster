from datetime import datetime, timezone
from typing import Any, Optional, TYPE_CHECKING
import secrets
from sqlmodel import Column, Field, SQLModel, Relationship, DateTime
from .enums import ReservationStatus

if TYPE_CHECKING:
    from .consumer import Consumer
    from .bundlePosting import BundlePosting

# This function is used to generate a claim code for the Reservations
def generate_claim_code() -> str:
    # Generate a 10 char long code
    # 1, I, 0 and O is removed for simplicity
    alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    return "".join(secrets.choice(alphabet) for _ in range(10))

# The database table model for Reservations
class Reservation(SQLModel, table=True):
    reservation_id: Optional[int] = Field(default=None, primary_key=True,index=True)
    posting_id: Optional[int] = Field(default=None, foreign_key="bundleposting.posting_id", index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="consumer.user_id", index=True)
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc)
    )
    status: ReservationStatus = Field(default=ReservationStatus.RESERVED)
    #Here we assign claim code
    claim_code: str = Field(
        default_factory=generate_claim_code,
        unique=True,
        index=True
    )

    # These are automatic relationships to other tables
    consumer: "Consumer" = Relationship(back_populates="reservations")
    posting: "BundlePosting" = Relationship(back_populates="reservations")