"""

Tests the seller-facing operations: creating, updating, and deleting
food-waste bundles. Covers schema-level input validation (negative
prices, time-window ordering), ownership authorisation, cascade
deletion of child rows, and the pickup-window string generation.

"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch, call
from fastapi import HTTPException
from pydantic import ValidationError

from app.services import bundlePosting as bundlePosting_service
from app.crud import bundlePosting as bundlePosting_crud




@pytest.fixture
def mock_db():
    """Provides a MagicMock that stands in for the SQLModel Session."""
    return MagicMock()


# ── A-S03: Bundle Creation Validation ─────────────────────────────────
# These tests verify that the BundlePostingCreate schema rejects
# obviously invalid data before it ever reaches the service/CRUD layer.
# Each test constructs a real Pydantic model and asserts that
# ValidationError is raised with a message mentioning the bad field.

def test_bundle_negative_price_rejected():
    """
    A negative price must be rejected by the schema.

    """
    from app.schemas.bundlePosting import BundlePostingCreate
    from app.schemas.category import CategoryPublic

    now = datetime.now(timezone.utc)

    with pytest.raises(ValidationError) as exc:
        BundlePostingCreate(
            user_id=1,
            category=CategoryPublic(category_id=1, name="Test"),
            allergens=None,
            available=10,
            price=-5.00,
            weight=500,
            start_time=now + timedelta(hours=1),
            end_time=now + timedelta(hours=3),
        )
    assert "price" in str(exc.value).lower()


def test_bundle_zero_price_rejected():
    """
    A zero price must also be rejected (free items aren't supported).

    
    """
    from app.schemas.bundlePosting import BundlePostingCreate
    from app.schemas.category import CategoryPublic

    now = datetime.now(timezone.utc)

    with pytest.raises(ValidationError) as exc:
        BundlePostingCreate(
            user_id=1,
            category=CategoryPublic(category_id=1, name="Test"),
            allergens=None,
            available=10,
            price=0,
            weight=500,
            start_time=now + timedelta(hours=1),
            end_time=now + timedelta(hours=3),
        )
    assert "price" in str(exc.value).lower()


def test_bundle_end_before_start_rejected():
    """
    end_time earlier than start_time must be rejected.

   
    """
    from app.schemas.bundlePosting import BundlePostingCreate
    from app.schemas.category import CategoryPublic

    now = datetime.now(timezone.utc)

    with pytest.raises(ValidationError) as exc:
        BundlePostingCreate(
            user_id=1,
            category=CategoryPublic(category_id=1, name="Test"),
            allergens=None,
            available=10,
            price=3.00,
            weight=500,
            start_time=now + timedelta(hours=3),
            end_time=now + timedelta(hours=1),
        )
    assert "end_time must be after start_time" in str(exc.value)


# ── A-S01: Ownership Guard ───────────────────────────────────────────
# Sellers must only be able to update their own bundles. The service
# compares posting.user_id with the caller's user_id and raises 403
# on mismatch.

def test_update_bundle_wrong_owner_raises_403(mock_db):
    """
    Updating a bundle you do NOT own raises HTTP 403.

    
    """
    from app.schemas.bundlePosting import BundlePostingUpdate

    mock_bundle = MagicMock()
    mock_bundle.user_id = 1
    mock_bundle.pickup_window = MagicMock()
    mock_bundle.pickup_window.lower = datetime.now(timezone.utc)
    mock_bundle.pickup_window.upper = datetime.now(timezone.utc) + timedelta(hours=4)

    update = BundlePostingUpdate(available=5)

    with patch.object(bundlePosting_crud, "get_bundle_posting", return_value=mock_bundle):
        with pytest.raises(HTTPException) as exc:
            bundlePosting_service.update_bundle_posting(
                posting_id=1, bundle_update=update, db=mock_db, user_id=999
            )
        assert exc.value.status_code == 403


def test_update_bundle_correct_owner_succeeds(mock_db):
    """
    Updating a bundle you own calls through to the CRUD layer.

    
    """
    from app.schemas.bundlePosting import BundlePostingUpdate

    mock_bundle = MagicMock()
    mock_bundle.user_id = 1
    mock_bundle.pickup_window = MagicMock()
    mock_bundle.pickup_window.lower = datetime.now(timezone.utc)
    mock_bundle.pickup_window.upper = datetime.now(timezone.utc) + timedelta(hours=4)

    update = BundlePostingUpdate(available=5)

    with patch.object(bundlePosting_crud, "get_bundle_posting", return_value=mock_bundle), \
         patch.object(bundlePosting_crud, "update_bundle_posting", return_value=mock_bundle) as mock_update:
        bundlePosting_service.update_bundle_posting(
            posting_id=1, bundle_update=update, db=mock_db, user_id=1
        )
        mock_update.assert_called_once()


# ── A-S06: Deletion Integrity ────────────────────────────────────────
# Deleting a bundle must also remove all related rows: reservations,
# issue reports, and the forecast. The service iterates child
# collections and calls the appropriate delete functions before
# marking the bundle itself as deleted.

def test_delete_bundle_clears_reservations(mock_db):
    """
    Deleting a bundle cascades to its reservations, reports, and forecast.

    
    """
    mock_reservation = MagicMock()
    mock_reservation.reservation_id = 10

    mock_report = MagicMock()
    mock_report.issue_id = 20

    mock_forecast = MagicMock()
    mock_forecast.forecast_id = 30

    mock_bundle = MagicMock()
    mock_bundle.posting_id = 1
    mock_bundle.reservations = [mock_reservation]
    mock_bundle.reports = [mock_report]
    mock_bundle.forecast = mock_forecast

    with patch.object(bundlePosting_crud, "get_bundle_posting", return_value=mock_bundle), \
         patch("app.services.reservation.delete_reservation") as mock_del_res, \
         patch("app.services.issueReport.delete_issue_report") as mock_del_report, \
         patch("app.services.forecast.delete_forecast") as mock_del_forecast, \
         patch.object(bundlePosting_crud, "set_bundle_deleted", return_value=mock_bundle):

        bundlePosting_service.set_bundle_deleted(posting_id=1, db=mock_db)

        mock_del_res.assert_called_once_with(reservation_id=10, db=mock_db)
        mock_del_report.assert_called_once_with(issue_id=20, db=mock_db)
        mock_del_forecast.assert_called_once_with(forecast_id=30, db=mock_db)


def test_delete_bundle_with_no_reservations(mock_db):
    """
    Deleting a bundle that has no child reservations or reports still
    succeeds without errors.

    """
    mock_forecast = MagicMock()
    mock_forecast.forecast_id = 30

    mock_bundle = MagicMock()
    mock_bundle.posting_id = 1
    mock_bundle.reservations = []
    mock_bundle.reports = []
    mock_bundle.forecast = mock_forecast

    with patch.object(bundlePosting_crud, "get_bundle_posting", return_value=mock_bundle), \
         patch("app.services.forecast.delete_forecast") as mock_del_forecast, \
         patch.object(bundlePosting_crud, "set_bundle_deleted", return_value=mock_bundle) as mock_set:

        bundlePosting_service.set_bundle_deleted(posting_id=1, db=mock_db)

        mock_del_forecast.assert_called_once()
        mock_set.assert_called_once()


# ── A-S05: Bundle Creation Service ───────────────────────────────────
# The service converts the schema's start_time / end_time into a
# PostgreSQL TSTZRANGE string and forwards it to the CRUD layer.

def test_create_bundle_generates_pickup_range(mock_db):
    """
    create_bundle_posting converts start/end times into a
    pickup_window range string for PostgreSQL.

    
    """
    now = datetime.now(timezone.utc)
    mock_bundle_in = MagicMock()
    mock_bundle_in.start_time = now + timedelta(hours=1)
    mock_bundle_in.end_time = now + timedelta(hours=3)

    mock_bundle = MagicMock()
    mock_bundle.posting_id = 1

    with patch.object(bundlePosting_crud, "create_bundle_posting", return_value=mock_bundle) as mock_create, \
         patch("app.services.forecast.create_forecast"):

        bundlePosting_service.create_bundle_posting(
            bundle_in=mock_bundle_in, owner_id=1, db=mock_db
        )

        # Verify pickup_window string was built from start/end times
        _, kwargs = mock_create.call_args
        assert mock_bundle_in.start_time.isoformat() in kwargs["pickup_window"]
        assert mock_bundle_in.end_time.isoformat() in kwargs["pickup_window"]


# ── A-S03 (extended): Bundle Update Time-Window Validation ────────────
# The BundlePostingUpdate schema uses a @model_validator to ensure
# end_time is strictly after start_time when both are provided.
# This prevents sellers from accidentally creating impossible pickup
# windows that could confuse consumers.

def test_time_window_validation_end_before_start():
    """
    Providing an end_time that is earlier than start_time must raise
    a ValidationError at schema level.
    
    """
    from app.schemas.bundlePosting import BundlePostingUpdate

    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError) as exc:
        BundlePostingUpdate(
            start_time=now + timedelta(hours=2),
            end_time=now + timedelta(hours=1),  # end BEFORE start
        )
    assert "end_time must be after start_time" in str(exc.value)


def test_time_window_equal_start_end_rejected():
    """
    start_time == end_time is also rejected because a zero-length
    pickup window is meaningless.
   
    """
    from app.schemas.bundlePosting import BundlePostingUpdate

    now = datetime.now(timezone.utc)
    same = now + timedelta(hours=1)
    with pytest.raises(ValidationError) as exc:
        BundlePostingUpdate(start_time=same, end_time=same)
    assert "end_time must be after start_time" in str(exc.value)


def test_time_window_valid_update_passes(mock_db):
    """
    A valid time window (end > start) passes schema validation and
    the service calls the CRUD update function.
   
    """
    from app.schemas.bundlePosting import BundlePostingUpdate

    now = datetime.now(timezone.utc)
    update = BundlePostingUpdate(
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=3),
    )

    mock_bundle = MagicMock()
    mock_bundle.user_id = 1
    mock_bundle.pickup_window = MagicMock()
    mock_bundle.pickup_window.lower = now
    mock_bundle.pickup_window.upper = now + timedelta(hours=4)

    with patch.object(bundlePosting_crud, "get_bundle_posting", return_value=mock_bundle):
        with patch.object(
            bundlePosting_crud, "update_bundle_posting", return_value=mock_bundle
        ) as mock_update:
            bundlePosting_service.update_bundle_posting(
                posting_id=1, bundle_update=update, db=mock_db, user_id=1
            )
            mock_update.assert_called_once()
