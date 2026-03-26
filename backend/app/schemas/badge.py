from sqlmodel import SQLModel

# The base schema for badges
class BadgeBase(SQLModel):
    name: str
    detail: str

# The public schema for badges
# Inherits from base
class BadgePublic(BadgeBase):
    badge_id: int