import json
import os

from fastapi import APIRouter, HTTPException

from backend.app.api.deps import AdminDep


router = APIRouter()

@router.get("/tests")
def get_test_results(admin: AdminDep):
    if not os.path.exists("test_results.json"):
        raise HTTPException(status_code=404, detail="No test results available yet")
    with open("test_results.json") as f:
        return json.load(f)