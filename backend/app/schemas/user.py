from pydantic import field_validator
from sqlmodel import SQLModel

from app.models.enums import Role

# The base schema for users
class UserBase(SQLModel):
    email: str

    @field_validator("email")
    @classmethod
    def strip_email(cls, v: str) -> str:
        return v.strip()

# The create schema for users
class UserCreate(UserBase):
    password: str

# The schema used to update a user
class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None

# The schema used by admins to update a user
class UserAdminUpdate(UserUpdate):
    pass

# The public schema for users
class UserPublic(UserBase):
    user_id: int
    role: Role