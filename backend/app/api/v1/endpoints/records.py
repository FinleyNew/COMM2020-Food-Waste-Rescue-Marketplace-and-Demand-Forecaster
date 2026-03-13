from fastapi import APIRouter, HTTPException
from app.api.deps import AdminDep, SellerDep, SessionDep
from app.schemas.record import RecordAdminUpdate, RecordPublic
from app.services import record as record_service
from typing import List

router = APIRouter()

@router.get("/", response_model=list[RecordPublic])
def get_all_records(current_user: AdminDep, db: SessionDep):
    return record_service.get_all_records(db=db)

@router.patch("/admin/{record_id}", response_model=RecordPublic)
def admin_update_record(record_id: int, record_update: RecordAdminUpdate, current_user: AdminDep, db: SessionDep):
    return record_service.update_record(record_id=record_id, record_update=record_update, db=db)

# Endpoint for getting the current sellers records
@router.get("/me", response_model= List[RecordPublic])
def get_current_sellers_records(current_seller: SellerDep, db: SessionDep):
    return current_seller.records or []

@router.delete("/{record_id}")
def delete_record(record_id: int, current_user: AdminDep, db: SessionDep):
    record_service.delete_record(record_id=record_id, db=db)