from sqlmodel import SQLModel

class BadgeBase(SQLModel):
    name: str
    detail: str

class BadgePublic(BadgeBase):
    pass