from fastapi import APIRouter
from app.api.deps import ConsumerDep, SessionDep
from app.schemas.consumer import ConsumerPublic
from app.services import user as user_service
from app.services import consumer as consumer_service

router = APIRouter()

@router.get("/me", response_model = ConsumerPublic)
def get_current_consumer(current_consumer: ConsumerDep, db: SessionDep):
    consumer_id = current_consumer.user_id
    if current_consumer.streak > 0 and consumer_id:
        consumer_service.check_streak(consumer_id=consumer_id, db=db)
    return current_consumer