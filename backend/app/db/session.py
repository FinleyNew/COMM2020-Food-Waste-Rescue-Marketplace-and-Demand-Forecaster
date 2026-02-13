from sqlmodel import create_engine
from app.core.config import settings

# Get the database URL from settings
DATABASE_URL = settings.DATABASE_URL

# Create the engine with that URL
# echo = True makes it add to log
engine = create_engine(DATABASE_URL, echo=True)