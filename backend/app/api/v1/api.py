from fastapi import APIRouter
from app.api.v1.endpoints import consumers, sellers, reservations, records, forecasts, login, users, bundlesPostings, categories, issueReports, admins

api_router = APIRouter()

#This file will route a request to the corresponding endpoint based on the prefix

api_router.include_router(consumers.router, prefix = "/consumers", tags=["consumers"])
api_router.include_router(sellers.router, prefix = "/sellers", tags=["sellers"])
api_router.include_router(bundlesPostings.router, prefix = "/bundles", tags=["bundles"])
api_router.include_router(reservations.router, prefix = "/reservations", tags=["reservations"])
api_router.include_router(records.router, prefix = "/records", tags=["records"])
api_router.include_router(forecasts.router, prefix = "/forecasts", tags=["forecasts"])
api_router.include_router(login.router, prefix = "/login", tags=["login"])
api_router.include_router(users.router, prefix = "/users", tags=["users"])
api_router.include_router(categories.router, prefix= "/categories", tags=["categories"])
api_router.include_router(admins.router, prefix="/admins", tags=["admins"])
api_router.include_router(issueReports.router, prefix="/reports", tags=["reports"])
