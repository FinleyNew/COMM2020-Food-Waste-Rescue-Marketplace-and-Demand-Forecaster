from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .enums import ReportStatus

if TYPE_CHECKING:
    from .consumer import Consumer
    from .bundlePosting import BundlePosting

class IssueReport(SQLModel, table=True):
    issue_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    posting_id: Optional[int] = Field(default=None, foreign_key="bundleposting.posting_id", index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="consumer.user_id", index=True)
    description: str
    status: ReportStatus = Field(default=ReportStatus.AWAITING_RESPONSE)
    seller_response: str | None = Field(default=None)

    consumer: "Consumer" = Relationship(back_populates="reports")
    posting: "BundlePosting" = Relationship(back_populates="reports")