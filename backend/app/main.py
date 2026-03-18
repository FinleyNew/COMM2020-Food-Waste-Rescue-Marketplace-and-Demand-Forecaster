from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.api.v1.api import api_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from app.core.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()

app = FastAPI(
    title="Prototype API",
    # This keeps the token saved even if you refresh the browser
    swagger_ui_parameters={"persistAuthorization": True},
    lifespan=lifespan
)



# Middleware so the backend can talk to the frontend on the same device
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes any requests to api.py
app.include_router(api_router, prefix="/api/v1")