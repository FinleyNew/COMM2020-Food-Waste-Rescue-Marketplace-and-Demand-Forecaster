from sqlmodel import SQLModel

class ForcastBase(SQLModel):
    user_id: int
    posting_id: int
    predicted_reservations: int
    predicted_no_show_prob: ?

class ForecastCreate(ForcastBase):
    pass

class ForecastPublic(ForcastBase):
    forecast_id: int