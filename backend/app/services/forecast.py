from sqlmodel import Session
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud import record as record_crud


def create_forecast(bundle_in: BundlePostingCreate, owner_id: int, pickup_range: str, db: Session):
    return

def get_forecast(bundle_in: BundlePostingCreate, db: Session):
    search_start = bundle_in.start_time.time()
    search_end = bundle_in.end_time.time()
    #Get any data you need from records
    #Use record_crud.get_all_records(db=db) to get all records for training the model
    #Use record_crud.get_same_time_records(search_start=search_start, search_end=search_end, day_of_week=?, db=db)
    #For day_of_week 0 is Sunday and 6 is Saturday
    # current_dow = (datetime.now().weekday() + 1) % 7 Get's the current dow in that form
    #Process that data into something usable
    #Call the create_forecast crud function to actually add it to the database
    return