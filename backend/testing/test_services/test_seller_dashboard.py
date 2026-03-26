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



# These tests verify that the BundlePostingCreate schema rejects obviously invalid data before it ever reaches the service/CRUD layer.


def test_bundle_negative_price_rejected():
    # The schema should reject bundles with negative prices, which don't make sense in the marketplace context.
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
            initial_price=10.00,
            contents="test content"
        )
    assert "price" in str(exc.value).lower()


def test_bundle_zero_price_rejected():
    # The schema should also reject zero prices, as free bundles could be abused and don't fit the marketplace model.
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
            initial_price=10.00,
            contents="test content"
        )
    assert "price" in str(exc.value).lower()


def test_bundle_end_before_start_rejected():
    # The schema should reject bundles where the end_time is before the start_time, as this would create an impossible pickup window.
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
            initial_price=10.00,
            contents="test content"
        )
    assert "end_time must be after start_time" in str(exc.value)



# Sellers must only be able to update their own bundles. The

def test_update_bundle_wrong_owner_raises_403(mock_db):
    # If a seller tries to update a bundle they don't own, the service must raise an HTTPException with status code 403 Forbidden.
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
    # If a seller updates their own bundle, the service should call the CRUD update function and return the updated bundle.
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





def test_delete_bundle_clears_reservations(mock_db):
    # When a bundle is deleted, the service must delete all associated reservations, issue reports, and forecasts to maintain data integrity and prevent orphaned records.
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
    # The service should still delete the bundle even if there are no associated reservations, reports, or forecasts.
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




def test_create_bundle_generates_pickup_range(mock_db):
    # When creating a bundle, the service must generate a pickup_window string in the format "start_iso - end_iso" based on the start_time and end_time provided in the input schema. This string is used for display purposes and must be correctly formatted.
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




def test_time_window_validation_end_before_start():
    # The schema should reject updates where the end_time is before the start_time, and the error message should mention the relevant fields for clarity.
    from app.schemas.bundlePosting import BundlePostingUpdate

    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError) as exc:
        BundlePostingUpdate(
            start_time=now + timedelta(hours=2),
            end_time=now + timedelta(hours=1),  # end BEFORE start
        )
    assert "end_time must be after start_time" in str(exc.value)


def test_time_window_equal_start_end_rejected():
    # The schema should also reject updates where the end_time is equal to the start_time, as this would create a zero-length pickup window. The error message should still mention the relevant fields.
    from app.schemas.bundlePosting import BundlePostingUpdate

    now = datetime.now(timezone.utc)
    same = now + timedelta(hours=1)
    with pytest.raises(ValidationError) as exc:
        BundlePostingUpdate(start_time=same, end_time=same)
    assert "end_time must be after start_time" in str(exc.value)


def test_time_window_valid_update_passes(mock_db):
    # If the update has a valid time window (end_time after start_time), the service should call the CRUD update function without raising an error. This test doesn't check the full update logic, just that valid times are accepted and passed through.
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
