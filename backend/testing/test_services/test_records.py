"""

Tests the historical-record management layer: creating, updating,
and deleting records, plus the Pydantic schema validators that
enforce business rules (end_time > start_time, positive weight, etc.).

"""

import pytest
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pydantic import ValidationError

from app.services import record as record_service
from app.schemas.record import RecordCreate, RecordAdminUpdate
from app.schemas.category import CategoryPublic


@pytest.fixture
def mock_db():
    
    return MagicMock()


def _valid_category():
    
    return CategoryPublic(name="bakery", category_id=1)


def _base_fields(**overrides):
    
    defaults = dict(
        user_id=1,
        posting_id=10,
        category=_valid_category(),
        price=Decimal("2.50"),
        raining=False,
        observed_reservations=3,
        observed_no_show=0,
        observed_expired=1,
        weight=500,
    )
    defaults.update(overrides)
    return defaults



# RecordCreate adds start_time / end_time with a model-validator that
# ensures end > start.

def test_record_create_valid(mock_db):
    
    now = datetime.now(timezone.utc)
    record = RecordCreate(
        **_base_fields(),
        start_time=now,
        end_time=now + timedelta(hours=1),
    )
    assert record.end_time > record.start_time


def test_record_create_end_before_start_raises():
    
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError, match="end_time must be after start_time"):
        RecordCreate(
            **_base_fields(),
            start_time=now,
            end_time=now - timedelta(hours=1),
        )


def test_record_create_zero_weight_rejected():
    
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        RecordCreate(
            **_base_fields(weight=0),
            start_time=now,
            end_time=now + timedelta(hours=1),
        )


def test_record_create_negative_reservations_rejected():
    
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        RecordCreate(
            **_base_fields(observed_reservations=-1),
            start_time=now,
            end_time=now + timedelta(hours=1),
        )



# RecordAdminUpdate only validates end > start when *both* are provided.

def test_admin_update_both_times_valid():
    
    now = datetime.now(timezone.utc)
    update = RecordAdminUpdate(
        start_time=now,
        end_time=now + timedelta(hours=2),
    )
    assert update.end_time > update.start_time


def test_admin_update_both_times_invalid_raises():
    
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError, match="end_time must be after start_time"):
        RecordAdminUpdate(
            start_time=now,
            end_time=now - timedelta(minutes=5),
        )


def test_admin_update_only_start_time_skips_validation():
    
    now = datetime.now(timezone.utc)
    update = RecordAdminUpdate(start_time=now)
    assert update.start_time == now
    assert update.end_time is None



# The service merges the incoming partial update with the existing
# record's pickup_window and re-validates end > start.

def test_update_record_valid_times(mock_db):
    
    now = datetime.now(timezone.utc)
    mock_record = MagicMock()
    mock_record.pickup_window.lower = now
    mock_record.pickup_window.upper = now + timedelta(hours=1)
    mock_updated = MagicMock()

    update_in = RecordAdminUpdate(end_time=now + timedelta(hours=2))

    with patch("app.crud.record.get_record_by_id", return_value=mock_record), \
         patch("app.crud.record.update_record", return_value=mock_updated) as mock_crud:
        result = record_service.update_record(record_id=1, record_update=update_in, db=mock_db)
        mock_crud.assert_called_once()
        assert result is mock_updated


def test_update_record_end_before_start_raises_400(mock_db):
    
    now = datetime.now(timezone.utc)
    mock_record = MagicMock()
    mock_record.pickup_window.lower = now + timedelta(hours=2)
    mock_record.pickup_window.upper = now + timedelta(hours=3)

    # Send a new end_time that is BEFORE the existing start
    update_in = RecordAdminUpdate(end_time=now)

    with patch("app.crud.record.get_record_by_id", return_value=mock_record):
        with pytest.raises(HTTPException) as exc_info:
            record_service.update_record(record_id=1, record_update=update_in, db=mock_db)
        assert exc_info.value.status_code == 400
        assert "end_time must be after start_time" in exc_info.value.detail


# ── R-04: create_record Service Logic ─────────────────────────────────

def test_create_record_passes_seller_coordinates(mock_db):
    
    mock_posting = MagicMock()
    mock_posting.seller.latitude = 50.72
    mock_posting.seller.longitude = -3.53
    mock_created = MagicMock()

    with patch("app.crud.record.create_record", return_value=mock_created) as mock_crud:
        result = record_service.create_record(bundle_posting=mock_posting, db=mock_db)
        mock_crud.assert_called_once_with(
            bundle_posting=mock_posting, latitude=50.72, longitude=-3.53, db=mock_db
        )
        assert result is mock_created



