from typing import Optional, TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User
    from .reservation import Reservation

class Consumer(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.user_id")
    display_name: str
    streak: int

    user: "User" = Relationship(back_populates="consumer")
    reservations: List["Reservation"] = Relationship(back_populates="consumer")