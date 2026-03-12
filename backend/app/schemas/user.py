from sqlmodel import SQLModel

from app.models.enums import Role

class UserBase(SQLModel):
    email: str

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