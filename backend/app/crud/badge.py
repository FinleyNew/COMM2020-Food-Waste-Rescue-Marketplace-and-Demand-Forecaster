from typing import Sequence
from sqlmodel import Session, select

from app.models.badge import Badge, ConsumerBadge

# The crud function for getting all the badges from the DB
def get_all_badges(db: Session) -> Sequence[Badge]:
    statement = select(Badge)
    return db.exec(statement).all()

# The crud function for awarding a specific badge to a specific user
def award_badge(badge_name: str, consumer_id: int, db: Session):
    # Get the badge
    badge = db.exec(select(Badge).where(Badge.name == badge_name)).first()
    if not badge:
        return
    
    # Check the consumer does not already have this badge
    existing = db.exec(
        select(ConsumerBadge)
        .where(ConsumerBadge.user_id == consumer_id)
        .where(ConsumerBadge.badge_id == badge.badge_id)
    ).first()
    if existing:
        return
    
    # Give the badge to the consumer
    consumer_badge = ConsumerBadge(
        user_id=consumer_id,
        badge_id=badge.badge_id # type: ignore
    )
    db.add(consumer_badge)
    db.commit()