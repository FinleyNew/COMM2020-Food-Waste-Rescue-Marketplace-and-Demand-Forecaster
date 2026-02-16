from typing import Optional
from sqlmodel import SQLModel

# The base schema for forecsasts
class ForecastBase(SQLModel):
    user_id: int
    posting_id: Optional[int] = None
    predicted_reservations: int
    predicted_no_show_prob: float

# The create schema for forecasts
class ForecastCreate(ForecastBase):
    # Just pass as there are no extra attributes needed
    pass

# The create schema for forecasts
class ForecastPublic(ForecastBase):
    forecast_id: Optional[int] = None