from fastapi import APIRouter
from app.api.v1.endpoints import consumers, sellers, reservations, records, forecasts, login
from backend.app.api.v1.endpoints import bundlesPostings

api_router = APIRouter()

api_router.include_router(consumers.router, prefix = "/consumers", tags=["consumers"])
api_router.include_router(sellers.router, prefix = "/sellers", tags=["sellers"])
api_router.include_router(bundlesPostings.router, prefix = "/bundles", tags=["bundles"])
api_router.include_router(reservations.router, prefix = "/reservations", tags=["reservations"])
api_router.include_router(records.router, prefix = "/records", tags=["records"])
api_router.include_router(forecasts.router, prefix = "/forecasts", tags=["forecasts"])
api_router.include_router(login.router, prefix = "/login", tags=["login"])