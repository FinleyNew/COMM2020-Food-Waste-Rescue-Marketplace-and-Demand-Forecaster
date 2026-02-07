from typing import Optional, TYPE_CHECKING
import secrets
from sqlmodel import Field, SQLModel, Relationship
from .enums import ReservationStatus

if TYPE_CHECKING:
    from .consumer import Consumer
    from .bundlePosting import BundlePosting

def generate_claim_code() -> str:
    #Generate a 10 char long code
    alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    return "".join(secrets.choice(alphabet) for _ in range(10))

class Reservation(SQLModel, table=True):
    reservation_id: Optional[int] = Field(default=None, primary_key=True)
    posting_id: Optional[int] = Field(default=None, foreign_key="bundleposting.posting_id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    timestamp: str
    status: ReservationStatus = Field(default=ReservationStatus.RESERVED)
    claim_code: str = Field(
        default_factory=generate_claim_code,
        unique=True,
        index=True
    )

    consumer: "Consumer" = Relationship(back_populates="reservation")
    posting: "BundlePosting" = Relationship(back_populates="reservation")