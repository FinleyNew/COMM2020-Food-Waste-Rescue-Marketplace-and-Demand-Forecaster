from sqlmodel import Session, select

from app.db import base  # This triggers the imports of all models
from app.db.session import engine

def init_db():
    base.metadata.create_all(bind=engine)
    print("Successfully created tables")

if __name__ == "__main__":
    init_db()