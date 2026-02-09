from sqlmodel import Session, select
from app.models import Consumer


def reset_consumers_streak(consumer_id: int, db: Session):
    statement = select(Consumer).where(Consumer.user_id == consumer_id)
    consumer = db.exec(statement).one()

    consumer.streak = 0

    db.add(consumer)