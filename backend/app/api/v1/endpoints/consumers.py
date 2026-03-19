from fastapi import APIRouter
from app.api.deps import AdminDep, ConsumerDep, SessionDep
from app.schemas.consumer import ConsumerAdminUpdate, ConsumerPublic, ConsumerUpdate, ConsumerCreate
from app.services import user as user_service
from app.services import consumer as consumer_service
from app.schemas.user import UserCreate
from app.schemas.badge import BadgePublic

router = APIRouter()

# Endpoint for getting the current consumer
@router.get("/me", response_model = ConsumerPublic)
def get_current_consumer(current_consumer: ConsumerDep, db: SessionDep):
    consumer_id = current_consumer.user_id
    if current_consumer.streak > 0 and consumer_id:
        # This will correct the streak by checking if it's in date
        consumer_service.check_streak(consumer_id=consumer_id, db=db)
    return current_consumer

@router.get("/", response_model=list[ConsumerPublic])
def get_all_consumers(current_user: AdminDep, db: SessionDep):
    return consumer_service.get_all_consumers(db=db)

@router.get("/me/badges", response_model=list[BadgePublic])
def get_current_consumers_badges(current_consumer: ConsumerDep, db: SessionDep):
    return current_consumer.badges

# Ednpoint for creating a new consumer
@router.post("/", response_model = ConsumerPublic)
def create_consumer(consumer_in: ConsumerCreate, user_in: UserCreate, db: SessionDep):
    return consumer_service.create_consumer(consumer_in=consumer_in, user_in=user_in, db=db)

@router.patch("/me", response_model=ConsumerPublic)
def update_consumer(current_consumer: ConsumerDep, consumer_update: ConsumerUpdate, db: SessionDep):
    return consumer_service.update_consumer(current_consumer=current_consumer, consumer_update=consumer_update, db=db)

@router.patch("/admin/{user_id}", response_model=ConsumerPublic)
def admin_update_consumer(user_id: int, consumer_update: ConsumerAdminUpdate, current_user: AdminDep, db: SessionDep):
    current_consumer = consumer_service.get_consumer_by_id(user_id=user_id, db=db)
    return consumer_service.update_consumer(current_consumer=current_consumer, consumer_update=consumer_update, db=db)

@router.delete("/me")
def delete_current_consumer(current_user: ConsumerDep, db: SessionDep):
    consumer_service.delete_consumer(user_id=current_user.user_id, db=db) # type: ignore

@router.delete("/{user_id}")
def delete_consumer(user_id: int, current_user: AdminDep, db: SessionDep):
    consumer_service.delete_consumer(user_id=user_id, db=db)