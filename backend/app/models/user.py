from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .enums import Role

if TYPE_CHECKING:
    from .seller import Seller
    from .consumer import Consumer

# The database table model for Users
class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    role: Role

    # These are automatic relationships to other tables
    seller: Optional["Seller"] = Relationship(back_populates="user")
    consumer: Optional["Consumer"] = Relationship(back_populates="user")