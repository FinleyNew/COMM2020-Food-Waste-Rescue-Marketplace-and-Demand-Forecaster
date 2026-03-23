from pydantic import field_validator
from sqlmodel import SQLModel

from app.models.enums import Role

class UserBase(SQLModel):
    email: str

    @field_validator("email")
    @classmethod
    def strip_email(cls, v: str) -> str:
        return v.strip()

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None

class UserAdminUpdate(UserUpdate):
    pass

class UserPublic(UserBase):
    user_id: int
    role: Role