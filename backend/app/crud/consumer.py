from sqlmodel import Session, select
from app.models import Consumer
from app.schemas.consumer import ConsumerUpdate, ConsumerAdminUpdate, ConsumerCreate

def update_consumer(current_consumer: Consumer, consumer_update: ConsumerUpdate | ConsumerAdminUpdate, db: Session) -> Consumer:
    update_data = consumer_update.model_dump(exclude_unset=True)
    current_consumer.sqlmodel_update(update_data)
    db.commit()
    db.refresh(current_consumer)
    return current_consumer

def get_consumer_by_id(user_id: int, db: Session) -> Consumer:
    statement = select(Consumer).where(Consumer.user_id == user_id)
    return db.exec(statement).one()

# Crud function for reseting the consumers streak to 0
def reset_consumers_streak(consumer_id: int, db: Session):
    statement = select(Consumer).where(Consumer.user_id == consumer_id)
    consumer = db.exec(statement).one()
    
    consumer.streak = 0

    db.add(consumer)

def increment_consumers_streak(consumer_id: int, db: Session):
    statement = select(Consumer).where(Consumer.user_id == consumer_id)
    consumer = db.exec(statement).one()

    consumer.streak += 1

    db.add(consumer)

def create_consumer(consumer_in: ConsumerCreate, user_id: int, db: Session) -> Consumer:
    db_consumer = Consumer.model_validate(consumer_in, update={"user_id": user_id})
    db.add(db_consumer)
    db.flush()
    db.refresh(db_consumer)
    return db_consumer

def delete_consumer(user_id: int, db: Session):
    statement = select(Consumer).where(Consumer.user_id == user_id)
    consumer = db.exec(statement).first()
    if consumer:
        db.delete(consumer)
        db.commit()