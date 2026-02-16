from sqlmodel import Session
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud import record as record_crud
from app.crud import forecast as forecast_crud
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from datetime import datetime
from app.schemas.forecast import ForecastPublic, ForecastCreate
import pandas as pd
import numpy as np


def create_forecast(bundle_in: BundlePostingCreate, posting_id: int | None, db: Session):
    forecast = get_forecast(bundle_in=bundle_in, db=db)
    create_forecast = ForecastCreate(
        user_id=forecast.user_id,
        posting_id=posting_id,
        predicted_reservations=forecast.predicted_reservations,
        predicted_no_show_prob=forecast.predicted_no_show_prob
    )
    forecast_crud.create_forecast(forecast=create_forecast, db=db)
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
    dow = (bundle_in.start_time.weekday() + 1) % 7
    hour = bundle_in.start_time.hour
    #Process that data into something usable
    df = create_dataframe(records)
    model_res, model_no_show = train_model(df)
    #Call the create_forecast crud function to actually add it to the database
    #This function needs to return a forecast in the type Forecast which has
    posting_id=getattr(bundle_in, "posting_id", 0)
    #user_id, posting_id, predicted_reservations and predicted_no_show_prob
    X_new = pd.DataFrame([{
        "user_id": str(bundle_in.user_id),
        "category": str(bundle_in.category),
        "price": np.log(float(bundle_in.price)),
        "raining": int(bool(getattr(bundle_in, "raining", False))),
        "hour_sin": np.sin(2*np.pi*hour/24),
        "hour_cos": np.cos(2*np.pi*hour/24),
        "dow": dow
    }])
    y_pred_res = float(model_res.predict(X_new)[0])
    y_pred_no_show = float(model_no_show.predict(X_new)[0])
    predicted_reservations = max(0, int(round(y_pred_res)))
    predicted_no_show_prob = min(1.0, max(0.0, y_pred_no_show / y_pred_res)) if y_pred_res > 0 else 0.0
    forecast = ForecastPublic(
        user_id=bundle_in.user_id,
        posting_id=posting_id,
        predicted_reservations=predicted_reservations,
        predicted_no_show_prob=predicted_no_show_prob
    )
    return forecast

def create_dataframe(records):
    user_ids = [str(r.user_id) for r in records]
    categories = [str(r.category) for r in records]
    prices = [np.log(float(r.price)) for r in records]
    raining = [int(bool(r.raining)) for r in records]
    hours = [r.pickup_window.lower.hour for r in records]
    dows  = [(r.pickup_window.lower.weekday() + 1) % 7 for r in records]
    hour_sin = [np.sin(2*np.pi*h/24) for h in hours]
    hour_cos = [np.cos(2*np.pi*h/24) for h in hours]
    observed_reservations = [float(r.observed_reservations) for r in records]
    observed_no_shows = [float(r.observed_no_show) for r in records]
    df = pd.DataFrame({
        'user_id': user_ids,
        'category': categories,
        'price': prices,
        'raining': raining,
        'hour_sin': hour_sin,
        'hour_cos': hour_cos,
        'dow': dows,
        'observed_reservations': observed_reservations,
        'observed_no_shows': observed_no_shows
    })
    return df

def train_model(df: pd.DataFrame):
    X = df.drop(columns=['observed_reservations', 'observed_no_shows'])
    y_res = df['observed_reservations']
    y_no_show = df['observed_no_shows']
    categorical = ["user_id", "category", "dow"]
    numeric = ["raining", "hour_sin", "hour_cos", "price"]
    preProcess_res = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric)
        ]
    )
    preProcess_no_show = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric)
        ]
    )
    clf_res = Pipeline([
        ("preprocess", preProcess_res),
        ("model", PoissonRegressor(alpha=0.1, max_iter=2000)),
    ])
    clf_no_show = Pipeline([
        ("preprocess", preProcess_no_show),
        ("model", PoissonRegressor(alpha=0.1, max_iter=2000)),
    ])
    clf_res.fit(X, y_res)
    clf_no_show.fit(X, y_no_show)
    return clf_res, clf_no_show

def get_baseline(train_df: pd.DataFrame, dow: int, start_time: int):
    mask = (train_df["dow"] == dow) & (train_df["start_time"] == start_time)
    subset = train_df.loc[mask, "observed_reservations"]
    if len(subset) > 0:
        return float(subset.mean())
    # fallback if no exact matches:
    return float(train_df["observed_reservations"].mean())