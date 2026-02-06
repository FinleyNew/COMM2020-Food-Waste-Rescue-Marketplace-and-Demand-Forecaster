from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .seller import Seller
    from .bundlePosting import BundlePosting

class Forecast(SQLModel, table=True):
    forecast_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    posting_id: Optional[int] = Field(default=None, foreign_key="bundleposting.posting_id")
    predicted_reservations: float
    predicted_no_show: float

    seller: "Seller" = Relationship(back_populates="forecast")
    posting: "BundlePosting" = Relationship(back_populates="forecast")