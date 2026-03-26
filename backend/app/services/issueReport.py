from typing import Sequence

from fastapi import HTTPException
from sqlmodel import Session

from app.models.issueReport import IssueReport
from app.schemas.issueReport import IssueReportCreate
from app.crud import issueReport as issueReport_crud

# Creates an issue report
def create_issue_report(issue_report_in: IssueReportCreate, consumer_id: int, db: Session) -> IssueReport:
    return issueReport_crud.create_issue_report(issue_report_in=issue_report_in, consumer_id=consumer_id, db=db)

# Adds a response to an issue report
def respond_to_issue_report(response: str, issue_id: int, seller_id: int, db: Session) -> IssueReport:
    report = issueReport_crud.get_issue_report(issue_id=issue_id, db=db)
    if report.posting.user_id != seller_id:
        raise HTTPException(status_code=403, detail="Current seller is not the owner of this reports bundle")
    return issueReport_crud.add_response(response=response, issue_id=issue_id, db=db)

# Gets all the consumers issue reports for a specified bundle
def get_consumer_issue_reports(bundle_id: int, consumer_id: int, db: Session) -> Sequence[IssueReport]:
    return issueReport_crud.get_consumer_issue_reports(bundle_id=bundle_id, consumer_id=consumer_id, db=db)

# Gets all the sellers issue reports for a specified bundle
def get_sellers_issue_reports(bundle_id: int, seller_id: int, db: Session) -> Sequence[IssueReport]:
    return issueReport_crud.get_sellers_issue_reports(bundle_id=bundle_id, seller_id=seller_id, db=db)

# Gets all the reports
def get_all_reports(db: Session):
    return issueReport_crud.get_all_reports(db=db)

# Sets an issue report's status to resolved
def set_issue_report_resolved(issue_id: int, consumer_id: int, db: Session) -> IssueReport:
    report = issueReport_crud.get_issue_report(issue_id=issue_id, db=db)
    if report.user_id != consumer_id:
        raise HTTPException(status_code=403, detail="Current consumer is not the owner of this issue report")
    return issueReport_crud.set_issue_report_resolved(issue_id=issue_id, db=db)

# Deletes a specified issue report
def delete_issue_report(issue_id: int, db: Session):
    issueReport_crud.delete_issue_report(issue_id=issue_id, db=db)