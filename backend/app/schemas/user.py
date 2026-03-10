from sqlmodel import SQLModel

from app.models.enums import Role

class UserBase(SQLModel):
    role: Role

class UserCreate(UserBase):
    email: str
    password: str

class UserPublic(UserBase):
    user_id: int