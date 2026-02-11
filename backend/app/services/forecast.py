from sqlmodel import Session
from app.schemas.bundlePosting import BundlePostingCreate


def create_forecast(bundle_in: BundlePostingCreate, owner_id: int, db: Session):
    #Get any data you need from records
    #Process that data into something usable
    #Call the create_forecast crud function to actually add it to the database
    return