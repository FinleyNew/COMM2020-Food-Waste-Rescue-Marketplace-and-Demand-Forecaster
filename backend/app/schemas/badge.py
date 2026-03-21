from sqlmodel import SQLModel

class BadgeBase(SQLModel):
    name: str
    detail: str

class BadgePublic(BadgeBase):
    badge_id: int