from fastapi import APIRouter
from app.api.deps import ConsumerDep, SessionDep
from app.schemas.consumer import ConsumerCreate, ConsumerPublic
from app.services import user as user_service
from app.services import consumer as consumer_service
from app.schemas.user import UserCreate

router = APIRouter()

# Endpoint for getting the current consumer
@router.get("/me", response_model = ConsumerPublic)
def get_current_consumer(current_consumer: ConsumerDep, db: SessionDep):
    consumer_id = current_consumer.user_id
    if current_consumer.streak > 0 and consumer_id:
        # This will correct the streak by checking if it's in date
        consumer_service.check_streak(consumer_id=consumer_id, db=db)
    return current_consumer

# Ednpoint for creating a new consumer
@router.post("/", response_model = ConsumerPublic)
def create_consumer(consumer_in: ConsumerCreate, user_in: UserCreate, db: SessionDep):
    return consumer_service.create_consumer(consumer_in=consumer_in, user_in=user_in, db=db)