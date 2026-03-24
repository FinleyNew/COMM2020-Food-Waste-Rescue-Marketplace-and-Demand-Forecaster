from typing import Sequence

from sqlmodel import Session, select
from app.schemas.forecast import ForecastCreate
from app.models import Forecast

# The crud function for getting all forecasts
def get_all_forecasts(db: Session) -> Sequence[Forecast]:
    statement = select(Forecast)
    return db.exec(statement).all()

# The crud function for creating a new forecast
def create_forecast(forecast: ForecastCreate, db: Session) -> Forecast:
    # Converts the Schema into a Model
    db_forecast = Forecast.model_validate(forecast)
    db.add(db_forecast)
    db.commit()
    db.refresh(db_forecast)
    return db_forecast

# The crud function for deleting a specific forecasts
def delete_forecast(forecast_id: int, db: Session):
    statement = select(Forecast).where(Forecast.forecast_id == forecast_id)
    forecast = db.exec(statement).first()
    if forecast:
        db.delete(forecast)
        db.commit()