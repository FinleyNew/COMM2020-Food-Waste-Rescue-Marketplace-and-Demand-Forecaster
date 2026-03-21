from sqlmodel import Session, select

from app.schemas.issueReport import IssueReportCreate
from app.models.issueReport import IssueReport
from app.models.enums import ReportStatus


def create_issue_report(issue_report_in: IssueReportCreate, consumer_id: int, db: Session) -> IssueReport:
    db_issue_report = IssueReport.model_validate(issue_report_in, update={"user_id": consumer_id})
    db.add(db_issue_report)
    db.commit()
    db.refresh(db_issue_report)
    return db_issue_report

def get_issue_report(issue_id: int, db: Session) -> IssueReport:
    statement = select(IssueReport).where(IssueReport.issue_id == issue_id)
    return db.exec(statement).one()

def add_response(response: str, issue_id: int, db: Session) -> IssueReport:
    statement = select(IssueReport).where(IssueReport.issue_id == issue_id)
    report = db.exec(statement).one()
    report.seller_response = response
    report.status = ReportStatus.SELLER_RESPONDED
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

def get_consumer_issue_report(bundle_id: int, consumer_id: int, db: Session) -> IssueReport | None:
    statement = select(IssueReport).where(IssueReport.posting_id == bundle_id).where(IssueReport.user_id == consumer_id)
    return db.exec(statement).first()