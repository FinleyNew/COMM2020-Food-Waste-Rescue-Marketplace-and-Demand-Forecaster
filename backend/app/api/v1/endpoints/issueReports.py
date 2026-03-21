from fastapi import APIRouter

from app.schemas.issueReport import IssueReportCreate, IssueReportPublic
from app.api.deps import ConsumerDep, SellerDep, SessionDep
from app.services import issueReport as issueReport_service

router = APIRouter()

@router.post("/", response_model=IssueReportPublic)
def create_issue_report(issue_report_in: IssueReportCreate, current_user: ConsumerDep, db: SessionDep):
    user_id = current_user.user_id
    if user_id:
        return issueReport_service.create_issue_report(issue_report_in=issue_report_in, consumer_id=user_id, db=db)
    
@router.patch("/{response}", response_model=IssueReportPublic)
def respond_to_issue_report(response: str, issue_id: int, current_seller: SellerDep, db: SessionDep):
    user_id = current_seller.user_id
    if user_id:
        return issueReport_service.respond_to_issue_report(response=response, issue_id=issue_id, seller_id=user_id, db=db)