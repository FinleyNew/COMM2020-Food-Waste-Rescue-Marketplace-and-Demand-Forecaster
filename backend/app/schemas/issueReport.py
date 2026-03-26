from sqlmodel import SQLModel

from app.models.enums import ReportStatus

# The base schema for issue
class IssueReportBase(SQLModel):
    posting_id: int
    description: str

# The create schema for issue reports
class IssueReportCreate(IssueReportBase):
    pass

# The public schema for issue reports
class IssueReportPublic(IssueReportBase):
    issue_id: int
    user_id: int
    seller_response: str | None = None
    status: ReportStatus = ReportStatus.AWAITING_RESPONSE