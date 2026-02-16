from sqlmodel import Session
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud import record as record_crud
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from pprint import pprint
import pandas as pd
import numpy as np


def create_forecast(bundle_in: BundlePostingCreate, owner_id: int, pickup_range: str, db: Session):
    return

def get_forecast(bundle_in: BundlePostingCreate, db: Session):
    search_start = bundle_in.start_time.time()
    search_end = bundle_in.end_time.time()
    #Get any data you need from records
    #Use record_crud.get_all_records(db=db) to get all records for training the model
    records = record_crud.get_all_records(db=db)
    #Use record_crud.get_same_time_records(search_start=search_start, search_end=search_end, day_of_week=?, db=db)
    same_time_records = record_crud.get_same_time_records(search_start=search_start, search_end=search_end, day_of_week=0, db=db)
    #For day_of_week 0 is Sunday and 6 is Saturday
    # current_dow = (datetime.now().weekday() + 1) % 7 Get's the current dow in that form
    current_dow = (datetime.now().weekday() + 1) % 7
    #Process that data into something usable
    user_ids = [str(r.user_id) for r in records]
    categories = [str(r.category) for r in records]
    prices = [np.log(float(r.price)) for r in records]
    raining = [int(bool(r.raining)) for r in records]
    hours = [r.pickup_window.lower.hour for r in records]
    dows  = [(r.pickup_window.lower.weekday() + 1) % 7 for r in records]
    hour_sin = [np.sin(2*np.pi*h/24) for h in hours]
    hour_cos = [np.cos(2*np.pi*h/24) for h in hours]
    observed_reservations = [float(r.observed_reservations) for r in records]
    df = pd.DataFrame({
        'user_id': user_ids,
        'category': categories,
        'price': prices,
        'raining': raining,
        'hour_sin': hour_sin,
        'hour_cos': hour_cos,
        'dow': dows,
        'observed_reservations': observed_reservations
    })
    model = train_model(df)
    #Call the create_forecast crud function to actually add it to the database
    #This function needs to return a forecast in the type Forecast which has
    #user_id, posting_id, predicted_reservations and predicted_no_show_prob
    return

def train_model(df: pd.DataFrame) -> Pipeline:
    X = df.drop(columns=['observed_reservations'])
    y = df['observed_reservations']
    categorical = ["user_id", "category", "dow"]
    numeric = ["raining", "hour_sin", "hour_cos", "price"]
    preProcess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric)
        ]
    )
    clf = Pipeline([
        ("preprocess", preProcess),
        ("model", PoissonRegressor(alpha=0.1, max_iter=2000)),
    ])
    clf.fit(X, y)
    return clf