from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .seller import Seller
    from .bundlePosting import BundlePosting

class Forecast(SQLModel, table=True):
    forecast_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="seller.user_id", index=True)
    posting_id: Optional[int] = Field(default=None, foreign_key="bundleposting.posting_id", index=True)
    predicted_reservations: int
    predicted_no_show_prob: float

    seller: "Seller" = Relationship(back_populates="forecasts")
    posting: "BundlePosting" = Relationship(back_populates="forecast")