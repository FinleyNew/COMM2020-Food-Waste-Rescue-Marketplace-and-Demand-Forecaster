from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Badge(SQLModel, table=True):
    badge_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    detail: str


class ConsumerBadge(SQLModel, table=True):
    badge_id: int = Field(foreign_key="badge.badge_id", default=None, primary_key=True)
    user_id: int = Field(foreign_key="consumer.user_id", default=None, primary_key=True, index=True)
    earned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))