"""

Tests the issue-report workflow: consumers create reports against
bundle postings, sellers respond, consumers mark them resolved, and
admins can delete. The service layer enforces ownership checks before
allowing sellers to respond or consumers to resolve.

"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services import issueReport as issue_service


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    
    return MagicMock()



# The seller who owns the posting can add a response.  Anyone else gets a 403.

def test_respond_to_issue_report_success(mock_db):
    
    mock_report = MagicMock()
    mock_report.posting.user_id = 5          
    mock_response = MagicMock()

    with patch("app.crud.issueReport.get_issue_report", return_value=mock_report), \
         patch("app.crud.issueReport.add_response", return_value=mock_response) as mock_add:
        result = issue_service.respond_to_issue_report(
            response="We'll replace it", issue_id=1, seller_id=5, db=mock_db
        )
        mock_add.assert_called_once_with(response="We'll replace it", issue_id=1, db=mock_db)
        assert result is mock_response


def test_respond_to_issue_report_wrong_seller_raises_403(mock_db):
    
    mock_report = MagicMock()
    mock_report.posting.user_id = 5         

    with patch("app.crud.issueReport.get_issue_report", return_value=mock_report):
        with pytest.raises(HTTPException) as exc_info:
            issue_service.respond_to_issue_report(
                response="hacked", issue_id=1, seller_id=999, db=mock_db
            )
        assert exc_info.value.status_code == 403



# The consumer who created the report can mark it resolved.  Anyone else gets a 403.
def test_set_issue_report_resolved_success(mock_db):
    
    mock_report = MagicMock()
    mock_report.user_id = 7                  
    mock_resolved = MagicMock()

    with patch("app.crud.issueReport.get_issue_report", return_value=mock_report), \
         patch("app.crud.issueReport.set_issue_report_resolved", return_value=mock_resolved) as mock_crud:
        result = issue_service.set_issue_report_resolved(
            issue_id=1, consumer_id=7, db=mock_db
        )
        mock_crud.assert_called_once_with(issue_id=1, db=mock_db)
        assert result is mock_resolved


def test_set_issue_report_resolved_wrong_consumer_raises_403(mock_db):
    
    mock_report = MagicMock()
    mock_report.user_id = 7                  # real owner

    with patch("app.crud.issueReport.get_issue_report", return_value=mock_report):
        with pytest.raises(HTTPException) as exc_info:
            issue_service.set_issue_report_resolved(
                issue_id=1, consumer_id=999, db=mock_db
            )
        assert exc_info.value.status_code == 403



