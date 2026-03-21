from sqlmodel import SQLModel

from app.models.enums import ReportStatus


class IssueReportBase(SQLModel):
    posting_id: int
    description: str

class IssueReportCreate(IssueReportBase):
    pass

class IssueReportPublic(IssueReportBase):
    issue_id: int
    user_id: int