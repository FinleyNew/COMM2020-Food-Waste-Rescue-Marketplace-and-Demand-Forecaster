from typing import Optional, TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User
    from .reservation import Reservation

# The database table model for Consumers
class Consumer(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.user_id", index=True)
    display_name: str
    streak: int = 0

    # These are automatic relationships to other tables
    user: "User" = Relationship(back_populates="consumer")
    reservations: List["Reservation"] = Relationship(back_populates="consumer")