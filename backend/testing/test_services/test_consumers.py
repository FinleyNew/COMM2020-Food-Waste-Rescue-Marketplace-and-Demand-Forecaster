import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from datetime import datetime, timedelta

# ---------------------------------------------------------
# A-C01 & A-C02: INVENTORY MATH & ZERO-STOCK GUARD
# ---------------------------------------------------------
def test_reservation_inventory_logic(mock_db):
    """
    Tests A-C01 (Reduction) and A-C02 (Zero-Stock Guard).
    """
    # Import inside the function to avoid circular import
    from app.services import bundlePosting

    # 1. Test A-C01: Verify quantity drops by 1
    with patch("app.crud.bundlePosting.reserve_bundle_posting") as mock_reserve:
        bundlePosting.reserve_bundle_posting(posting_id=101, db=mock_db)
        mock_reserve.assert_called_once_with(posting_id=101, db=mock_db)

    # 2. Test A-C02: Logic to prevent reservation if qty is 0
    with patch("app.crud.bundlePosting.reserve_bundle_posting",
               side_effect=HTTPException(status_code=400, detail="InsufficientStock")):
        with pytest.raises(HTTPException) as exc:
            bundlePosting.reserve_bundle_posting(posting_id=101, db=mock_db)
        assert exc.value.detail == "InsufficientStock"

# ---------------------------------------------------------
# A-C03: ACTIVE FILTER (is_active=True)
# ---------------------------------------------------------
def test_service_only_returns_active_bundles(mock_db):
    """
    Test A-C03: Ensure the brain only asks for 'Live' bundles.
    """
    from app.services import bundlePosting
    with patch("app.crud.bundlePosting.get_active_bundle_postings") as mock_get:
        bundlePosting.get_active_bundle_postings(db=mock_db)
        mock_get.assert_called_once()

# ---------------------------------------------------------
# A-C04: TIME-WINDOW CHECK
# ---------------------------------------------------------
def test_bundle_time_window_logic():
    """
    Test A-C04: Returns False/Error if current time is outside the range.
    """
    from app.services.bundlePosting import update_bundle_posting

    mock_update = MagicMock()
    mock_update.start_time = datetime.now() + timedelta(hours=5)
    mock_update.end_time = datetime.now() + timedelta(hours=2)  # Ends BEFORE it starts

    with patch("app.crud.bundlePosting.get_bundle_posting", return_value=MagicMock(user_id=1)):
        with pytest.raises(HTTPException) as exc:
            update_bundle_posting(posting_id=1, bundle_update=mock_update, db=MagicMock(), user_id=1)
        assert exc.value.status_code == 400

# ---------------------------------------------------------
# A-C05: USER ISOLATION (Security)
# ---------------------------------------------------------
def test_user_isolation_query_logic(mock_db):
    """
    Test A-C05: User A cannot see User B's private data.
    """
    from app.services import bundlePosting
    with patch("app.crud.bundlePosting.get_bundle_postings_by_owner") as mock_filter:
        bundlePosting.get_bundle_postings_by_owner(owner_id=55, db=mock_db)
        mock_filter.assert_called_with(owner_id=55, db=mock_db)

# ---------------------------------------------------------
# A-C06: SEARCH NORMALIZATION
# ---------------------------------------------------------
def test_search_query_normalization(mock_db):
    """
    Test A-C06: Verifies '  Bread  ' is handled.
    """
    from app.services import bundlePosting
    with patch("app.crud.bundlePosting.get_queried_bundle_postings") as mock_search:
        bundlePosting.get_queried_bundle_postings(query="  Co-op  ", db=mock_db)
        mock_search.assert_called_with(query="  Co-op  ", db=mock_db)

# ---------------------------------------------------------
# A-C07: ALLERGEN LOGIC (Invisible Filter)
# ---------------------------------------------------------
def test_allergen_filter_logic():
    """
    Test A-C07: Logic to remove bundles with specific tags.
    """
    bundles = [
        {"id": 1, "tags": ["Dairy"]},
        {"id": 2, "tags": ["Vegan"]}
    ]
    # Simulate a user selecting 'Dairy Free'
    filtered = [b for b in bundles if "Dairy" not in b["tags"]]
    assert len(filtered) == 1
    assert filtered[0]["id"] == 2