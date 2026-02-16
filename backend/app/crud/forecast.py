from sqlmodel import Session
from app.schemas.forecast import ForecastCreate
from app.models import Forecast

#Crud function for creating a forecast
def create_forecast(forecast: ForecastCreate, db: Session) -> Forecast:
    # Converts the Schema into a Model
    db_forecast = Forecast.model_validate(forecast)
    db.add(db_forecast)
    db.commit()
    db.refresh(db_forecast)
    return db_forecast