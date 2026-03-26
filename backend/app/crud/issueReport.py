from typing import Sequence

from sqlmodel import Session, select

from app.schemas.issueReport import IssueReportCreate
from app.models.issueReport import IssueReport
from app.models.enums import ReportStatus
from app.models.bundlePosting import BundlePosting

# The crud function for creating a new issue report
def create_issue_report(issue_report_in: IssueReportCreate, consumer_id: int, db: Session) -> IssueReport:
    db_issue_report = IssueReport.model_validate(issue_report_in, update={"user_id": consumer_id})
    db.add(db_issue_report)
    db.commit()
    db.refresh(db_issue_report)
    return db_issue_report

# The crud function for getting a specific issue report
def get_issue_report(issue_id: int, db: Session) -> IssueReport:
    statement = select(IssueReport).where(IssueReport.issue_id == issue_id)
    return db.exec(statement).one()

# The crud function for adding a response to a specific issue
def add_response(response: str, issue_id: int, db: Session) -> IssueReport:
    statement = select(IssueReport).where(IssueReport.issue_id == issue_id)
    report = db.exec(statement).one()
    report.seller_response = response
    report.status = ReportStatus.SELLER_RESPONDED
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

# The crud function for getting all of a specifc consumers issue reports
def get_consumer_issue_reports(bundle_id: int, consumer_id: int, db: Session) -> Sequence[IssueReport]:
    statement = select(IssueReport).where(IssueReport.posting_id == bundle_id).where(IssueReport.user_id == consumer_id)
    return db.exec(statement).all()

# The crud function for getting all of a specifc sellers issue reports
def get_sellers_issue_reports(bundle_id: int, seller_id: int, db: Session) -> Sequence[IssueReport]:
    statement = select(IssueReport).join(BundlePosting, IssueReport.posting_id == BundlePosting.posting_id).where(IssueReport.posting_id == bundle_id).where(BundlePosting.user_id == seller_id) # type: ignore
    return db.exec(statement).all()

# The crud function for getting all the issue reports
def get_all_reports(db: Session):
    statement = select(IssueReport)
    return db.exec(statement).all()

# The crud function for setting and issue report to resolved
def set_issue_report_resolved(issue_id: int, db: Session) -> IssueReport:
    statement = select(IssueReport).where(IssueReport.issue_id == issue_id)
    report = db.exec(statement).one()
    report.status = ReportStatus.RESOLVED
    db.add(report)
    db.commit()
    db.refresh(report)
    return report

# The crud function for deleting a specific issue report
def delete_issue_report(issue_id: int, db: Session):
    statement = select(IssueReport).where(IssueReport.issue_id == issue_id)
    report = db.exec(statement).first()

    if report:
        db.delete(report)
        db.commit()