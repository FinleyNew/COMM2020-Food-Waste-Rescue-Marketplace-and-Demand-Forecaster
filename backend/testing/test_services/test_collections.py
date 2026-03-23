"""

Tests the reservation creation workflow and the claim-code collection flow
in app.services.reservation. These are the core transactional paths that
move food bundles from "available" to "reserved" to "collected".

"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.services import reservation as reservation_service
from app.crud import reservation as reservation_crud
from app.models.enums import ReservationStatus


# ── Fixtures & Helpers ────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    
    return MagicMock()


def _mock_reservation(
    *,
    reservation_id: int = 1,
    consumer_id: int = 1,
    posting_id: int = 1,
    claim_code: str = "ABC123",
    status: str = "reserved",
    user_id: int = 1,
) -> MagicMock:
    # Returns a MagicMock that stands in for a Reservation object with the given attributes.
    res = MagicMock()
    res.reservation_id = reservation_id
    res.consumer_id = consumer_id
    res.user_id = user_id
    res.posting_id = posting_id
    res.claim_code = claim_code
    res.status = status
    return res



# The create_reservation service must:
#   1. Fetch the bundle with a row-level lock (lock=True) to prevent races
#   2. Reject the reservation when no stock is left (available <= 0)
#   3. Call reserve_bundle_posting to decrement stock
# These tests verify that  logic.

def test_create_reservation_checks_availability_and_reserves(mock_db):
    # The service should fetch the bundle with lock=True, check availability, and call reserve_bundle_posting if available.
    mock_res = _mock_reservation()
    mock_posting = MagicMock()
    mock_posting.available = 5
    mock_reservation_in = MagicMock()

    with patch.object(reservation_crud, "create_reservation", return_value=mock_res), \
         patch("app.services.reservation.get_bundle_posting", return_value=mock_posting) as mock_get, \
         patch("app.services.reservation.reserve_bundle_posting") as mock_reserve, \
         patch("app.services.badge.check_at_reservation"):
        result = reservation_service.create_reservation(
            reservation_in=mock_reservation_in, posting_id=1, consumer_id=1, db=mock_db
        )
        mock_get.assert_called_once_with(posting_id=1, db=mock_db, lock=True)
        mock_reserve.assert_called_once_with(posting_id=1, db=mock_db)


def test_create_reservation_rejects_zero_stock(mock_db):
    # If the bundle's available stock is 0 or less, the service should raise a ValueError and not create a reservation.
    mock_posting = MagicMock()
    mock_posting.available = 0
    mock_reservation_in = MagicMock()

    with patch("app.services.reservation.get_bundle_posting", return_value=mock_posting):
        with pytest.raises(ValueError, match="No bundles left"):
            reservation_service.create_reservation(
                reservation_in=mock_reservation_in, posting_id=1, consumer_id=1, db=mock_db
            )



# The collect_by_code service must:
#   1. Look up a reservation by its unique claim code
#   2. Reject already-collected reservations (400)
#   3. Reject no-show reservations (400)
#   4. Accept only RESERVED status and flip it to COLLECTED
#   5. Return 404 for non-existent claim codes

def test_collect_already_collected_raises_400(mock_db):
    # A reservation with status COLLECTED should not be collectible again — the service must raise HTTP 400.
    collected_res = _mock_reservation(status=ReservationStatus.COLLECTED)

    with patch.object(reservation_crud, "get_reservation_by_claim_code", return_value=collected_res):
        with pytest.raises(HTTPException) as exc:
            reservation_service.collect_by_code(
                claim_code="ABC123", db=mock_db
            )
        assert exc.value.status_code == 400
        assert "already been collected" in exc.value.detail


def test_collect_no_show_raises_400(mock_db):
    # A reservation marked as NO_SHOW (consumer failed to collect within
    # the pickup window) must not be collectible afterwards.
    
    no_show_res = _mock_reservation(status=ReservationStatus.NO_SHOW)

    with patch.object(reservation_crud, "get_reservation_by_claim_code", return_value=no_show_res):
        with pytest.raises(HTTPException) as exc:
            reservation_service.collect_by_code(
                claim_code="ABC123", db=mock_db
            )
        assert exc.value.status_code == 400
        assert "no-show" in exc.value.detail


def test_collect_valid_reservation_succeeds(mock_db):
    # A reservation with status RESERVED should be collectible, changing its status to COLLECTED.
    valid_res = _mock_reservation(status=ReservationStatus.RESERVED, user_id=1)

    with patch.object(reservation_crud, "get_reservation_by_claim_code", return_value=valid_res), \
         patch("app.services.badge.check_at_collection"):
        result = reservation_service.collect_by_code(
            claim_code="ABC123", db=mock_db
        )
        assert result.status == ReservationStatus.COLLECTED


def test_collect_invalid_code_raises_404(mock_db):
    # If no reservation exists with the provided claim code, the service should raise HTTP 404.
    with patch.object(reservation_crud, "get_reservation_by_claim_code", return_value=None):
        with pytest.raises(HTTPException) as exc:
            reservation_service.collect_by_code(
                claim_code="FAKE123", db=mock_db
            )
        assert exc.value.status_code == 404
