from sqlmodel import SQLModel

from app.models.enums import Role

class UserBase(SQLModel):
    pass

class UserCreate(UserBase):
    email: str
    password: str

class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None

class UserAdminUpdate(UserUpdate):
    pass

class UserPublic(UserBase):
    user_id: int
    role: Role