from typing import Sequence

from sqlmodel import Session
from app.schemas.bundlePosting import BundlePostingCreate
from app.crud import record as record_crud
from app.crud import forecast as forecast_crud
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from app.schemas.forecast import ForecastPublic, ForecastCreate
import pandas as pd
import numpy as np
from app.models.forecast import Forecast

# Gets all the forecasts
def get_all_forecasts(db: Session) -> Sequence[Forecast]:
    return forecast_crud.get_all_forecasts(db=db)

# Creates a new forecast
def create_forecast(bundle_in: BundlePostingCreate, posting_id: int | None, db: Session):
    #This function creates and stores a forecast object in the database for a given bundle posting
    forecast = get_forecast(bundle_in=bundle_in, db=db)
    #Object is created
    create_forecast = ForecastCreate(
        user_id=forecast.user_id,
        posting_id=posting_id,
        predicted_reservations=forecast.predicted_reservations,
        predicted_no_show_prob=forecast.predicted_no_show_prob
    )
    #Object is stored in the database
    forecast_crud.create_forecast(forecast=create_forecast, db=db)
    return

# Deletes a forecast
def delete_forecast(forecast_id: int, db: Session):
    forecast_crud.delete_forecast(forecast_id=forecast_id, db=db)

# Returns a forecast for the given bundle
def get_forecast(bundle_in: BundlePostingCreate, db: Session):
    search_start = bundle_in.start_time.time()
    search_end = bundle_in.end_time.time()
    #Get records to train the model
    records = record_crud.get_all_records(db=db)
    same_time_records = record_crud.get_same_time_records(search_start=search_start, search_end=search_end, day_of_week=0, db=db) # type: ignore
    #Collecting the day of week and starting time hour for the new bundle posting to make the prediction
    dow = (bundle_in.start_time.weekday() + 1) % 7
    hour = bundle_in.start_time.hour
    #Creating the dataframe and training the model
    df = create_dataframe(records)
    model_res, model_no_show = train_model(df)
    posting_id=getattr(bundle_in, "posting_id", 0)
    #Converting attributes to a usable format
    X_new = pd.DataFrame([{
        "user_id": str(bundle_in.user_id),
        "category": str(bundle_in.category),
        "price": np.log(float(bundle_in.price)),
        "raining": int(bool(getattr(bundle_in, "raining", False))),
        "hour_sin": np.sin(2*np.pi*hour/24),
        "hour_cos": np.cos(2*np.pi*hour/24),
        "dow": dow
    }])
    #Getting predictions for number of reservations and no show probability
    y_pred_res = float(model_res.predict(X_new)[0])
    y_pred_no_show = float(model_no_show.predict(X_new)[0])
    #Normalising the predictions so they can't be negative and the no show probability is between 0 and 1
    predicted_reservations = min(
        bundle_in.available,
        max(0, int(round(y_pred_res)))
    )
    predicted_no_show_prob = min(1.0, max(0.0, y_pred_no_show / y_pred_res)) if y_pred_res > 0 else 0.0
    #Creates the forecast and returns it
    forecast = ForecastPublic(
        user_id=bundle_in.user_id,
        posting_id=posting_id,
        predicted_reservations=predicted_reservations,
        predicted_no_show_prob=predicted_no_show_prob
    )
    #For calculating the model performance metrics, the evaluate_model function can be called which trains the model on 80% of the records and tests it on the remaining 20%, comparing the predictions to the actual observed reservations and no show rates. This is currently commented out to avoid long execution times when creating a forecast, but it can be uncommented for testing purposes.
    #print(evaluate_model(records))
    return forecast

def create_dataframe(records):
    #Parameters are transformed into a format that can be used to train the model.
    #Categorical variables are converted to strings, price is log transformed, hour is converted to sin and cos components and the day of week is calculated.
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
    #Dataframe is created with the transformed parameters
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
    #Observed reservations and observed no shows are dropped since these are the target variables we want to predict.
    X = df.drop(columns=['observed_reservations', 'observed_no_shows'])
    y_res = df['observed_reservations']
    y_no_show = df['observed_no_shows']
    #Categorical features and numeric features and separated
    categorical = ["user_id", "category", "dow"]
    numeric = ["raining", "hour_sin", "hour_cos", "price"]
    #Preprocessing pipelines are created for both the number of reservations and no show probability predictions, using a column transformer to apply one hot encoding to the categorical features
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
    #Pipelines are created for both predictions using a poisson regression model
    clf_res = Pipeline([
        ("preprocess", preProcess_res),
        ("model", PoissonRegressor(alpha=0.1, max_iter=2000)),
    ])
    clf_no_show = Pipeline([
        ("preprocess", preProcess_no_show),
        ("model", PoissonRegressor(alpha=0.1, max_iter=2000)),
    ])
    #Fit and return the models
    clf_res.fit(X, y_res)
    clf_no_show.fit(X, y_no_show)
    return clf_res, clf_no_show

def get_baseline(records, dow: int, start_time):
    #Find all records that match the same day of the week and starting hour
    matching = [
        r.observed_reservations
        for r in records
        if ((r.pickup_window.lower.weekday() + 1) % 7 == dow)
        and (r.pickup_window.lower.hour == start_time)
    ]
    #Checks if there are any matching records
    if len(matching) > 0:
        return float(sum(matching) / len(matching))

    return float(sum(r.observed_reservations for r in records) / len(records))

def evaluate_model(records):
    #Checks if there are enough records to train and test the model
        if len(records) < 2:
            return {
                "baseline_mae": None,
                "model_mae": None,
                "baseline_mse": None,
                "model_mse": None,
                "baseline_no_show_mae": None,
                "model_no_show_mae": None,
                "baseline_no_show_mse": None,
                "model_no_show_mse": None
            }

        #Splits the records into a training set and a test set
        split_index = int(len(records) * 0.8)

        train_records = records[:split_index]
        test_records = records[split_index:]

        train_df = create_dataframe(train_records)
        test_df = create_dataframe(test_records)

        model_res, model_no_show = train_model(train_df)

        model_preds = []
        baseline_preds = []
        actuals = []

        model_no_show_preds = []
        baseline_no_show_preds = []
        actual_no_show_rates = []

        #Iterates through the test records
        for r, (_, row) in zip(test_records, test_df.iterrows()):
            X_new = pd.DataFrame([{
                "user_id": row["user_id"],
                "category": row["category"],
                "price": row["price"],
                "raining": row["raining"],
                "hour_sin": row["hour_sin"],
                "hour_cos": row["hour_cos"],
                "dow": row["dow"]
            }])

            #Reservation prediction
            model_pred = float(model_res.predict(X_new)[0])
            baseline_pred = get_baseline(
                train_records,
                (r.pickup_window.lower.weekday() + 1) % 7,
                r.pickup_window.lower.hour
            )
            actual = float(r.observed_reservations)

            #Calculates the baseline no show probability
            model_preds.append(model_pred)
            baseline_preds.append(baseline_pred)
            actuals.append(actual)

            model_no_show_count = float(model_no_show.predict(X_new)[0])
            model_no_show_prob = (
                min(1.0, max(0.0, model_no_show_count / model_pred))
                if model_pred > 0 else 0.0
            )

            baseline_no_show_prob = get_no_show_baseline(
                train_records,
                (r.pickup_window.lower.weekday() + 1) % 7,
                r.pickup_window.lower.hour
            )

            actual_no_show_rate = (
                float(r.observed_no_show / r.observed_reservations)
                if r.observed_reservations > 0 else 0.0
            )

            #Append the no show predictions and actual rates to their respective lists
            model_no_show_preds.append(model_no_show_prob)
            baseline_no_show_preds.append(baseline_no_show_prob)
            actual_no_show_rates.append(actual_no_show_rate)

        #Returns the results of the evaluation
        return {
            "baseline_mae": mean_absolute_error(actuals, baseline_preds),
            "model_mae": mean_absolute_error(actuals, model_preds),
            "baseline_mse": mean_squared_error(actuals, baseline_preds),
            "model_mse": mean_squared_error(actuals, model_preds),
            "baseline_no_show_mae": mean_absolute_error(actual_no_show_rates, baseline_no_show_preds),
            "model_no_show_mae": mean_absolute_error(actual_no_show_rates, model_no_show_preds),
            "baseline_no_show_mse": mean_squared_error(actual_no_show_rates, baseline_no_show_preds),
            "model_no_show_mse": mean_squared_error(actual_no_show_rates, model_no_show_preds)
        }

def get_no_show_baseline(records, dow, start_hour):
    #Finds all records that match the same day of the week and starting hour
    rates = [
        (r.observed_no_show / r.observed_reservations)
        for r in records
        if r.observed_reservations > 0
        and ((r.pickup_window.lower.weekday() + 1) % 7 == dow)
        and (r.pickup_window.lower.hour == start_hour)
    ]

    #Checks if there are matching records and returns 0.0 if not
    if len(rates) > 0:
        return float(sum(rates) / len(rates))

    return 0.0