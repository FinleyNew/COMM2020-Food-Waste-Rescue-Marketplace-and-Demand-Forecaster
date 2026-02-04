from fastapi import APIRouter, Depends, HTTPexception
from sqlmodel import Session
from app.api.deps import ConsumerDep, SessionDep
from app.schemas.consumer import ConsumerPublic
from app.services import user as user_service
from app.services import consumer as consumer_service

router = APIRouter()

@router.get("/me", response_model = ConsumerPublic)
def get_current_consumer(current_consumer: ConsumerDep, db: SessionDep):
    return current_consumer