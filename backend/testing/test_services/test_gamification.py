"""

Tests the consumer gamification features: weekly streaks and achievement
badges. The streak system encourages regular collections; the badge
system rewards milestones (first reservation, consecutive days, weight
thresholds, etc.).

Streak tests exercise the real branching logic in
app.services.consumer (check_streak, increment_streak).

Badge tests exercise the real branching logic in
app.services.badge (check_good_start, check_on_a_roll, etc.) and
the CRUD duplicate-prevention in app.crud.badge (award_badge).
"""

import pytest
from datetime import date, timedelta, datetime, timezone
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from app.crud import badge as badge_crud
from app.services import badge as badge_service
from app.services import consumer as consumer_service
from app.models.enums import ReservationStatus


# ── Fixtures & Helpers ────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    
    return MagicMock()


def _mock_reservation_with_timestamp(*, days_ago: int = 0):
    
    res = MagicMock()
    ts = datetime.now(timezone.utc) - timedelta(days=days_ago)
    res.timestamp = ts
    res.status = ReservationStatus.COLLECTED
    return res


def _mock_collected_reservation(*, days_ago: int = 0, weight: int = 500):
    res = MagicMock()
    res.timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago)
    res.status = ReservationStatus.COLLECTED
    res.posting = MagicMock()
    res.posting.weight = weight
    res.posting.user_id = 1
    return res



# A consumer's streak increments once per calendar week when they make
# a reservation. check_streak returns True if the streak is still valid
# (last reservation was this week or last week), False otherwise.
# increment_streak only bumps the counter if the last reservation was
# in the previous week (avoids double-incrementing within the same week).

def test_check_streak_valid_this_week(mock_db):
    # A reservation placed earlier this week keeps the streak valid (check_streak returns True).
    mock_res = _mock_reservation_with_timestamp(days_ago=0)

    with patch("app.services.consumer.get_reservations_by_consumer", return_value=[mock_res]):
        result = consumer_service.check_streak(consumer_id=1, db=mock_db)
        assert result is True


def test_check_streak_valid_last_week(mock_db):
    # A reservation from 6 days ago is still within the current week, so the streak is valid (check_streak returns True).
    days_back = date.today().weekday() + 1  # guarantees previous week
    mock_res = _mock_reservation_with_timestamp(days_ago=days_back)

    with patch("app.services.consumer.get_reservations_by_consumer", return_value=[mock_res]):
        result = consumer_service.check_streak(consumer_id=1, db=mock_db)
        assert result is True


def test_increment_streak_when_zero(mock_db):
    # When streak is 0, increment_streak should call increment_consumers_streak to start the streak.
    with patch("app.crud.consumer.increment_consumers_streak") as mock_inc:
        consumer_service.increment_streak(consumer_id=1, streak=0, db=mock_db)
        mock_inc.assert_called_once_with(consumer_id=1, db=mock_db)


def test_increment_streak_when_positive_and_last_week(mock_db):
    # When streak > 0 and the last reservation was from last week, increment_streak should call increment_consumers_streak to continue the streak.
    days_back = date.today().weekday() + 1
    mock_res = _mock_reservation_with_timestamp(days_ago=days_back)

    with patch("app.services.consumer.get_reservations_by_consumer", return_value=[mock_res]), \
         patch("app.crud.consumer.increment_consumers_streak") as mock_inc:
        consumer_service.increment_streak(consumer_id=1, streak=3, db=mock_db)
        mock_inc.assert_called_once_with(consumer_id=1, db=mock_db)


def test_increment_streak_skips_if_same_week(mock_db):
    # When streak > 0 and the last reservation was already this week, the streak is NOT incremented again.
    
    mock_res = _mock_reservation_with_timestamp(days_ago=0)

    with patch("app.services.consumer.get_reservations_by_consumer", return_value=[mock_res]), \
         patch("app.crud.consumer.increment_consumers_streak") as mock_inc:
        consumer_service.increment_streak(consumer_id=1, streak=3, db=mock_db)
        mock_inc.assert_not_called()



# If the consumer has been inactive for more than two weeks the streak
# resets to zero. If they have no reservations at all, a 404 is raised.

def test_check_streak_resets_if_old(mock_db):
    # A reservation from 15 days ago is outside the 2-week threshold, so check_streak returns False and resets the streak to 0.
    mock_res = _mock_reservation_with_timestamp(days_ago=30)

    with patch("app.services.consumer.get_reservations_by_consumer", return_value=[mock_res]), \
         patch("app.crud.consumer.reset_consumers_streak") as mock_reset:
        result = consumer_service.check_streak(consumer_id=1, db=mock_db)
        assert result is False
        mock_reset.assert_called_once_with(consumer_id=1, db=mock_db)


def test_check_streak_raises_if_no_reservations(mock_db):
    # If the consumer has no reservations, check_streak should raise an HTTPException with status code 404.
    with patch("app.services.consumer.get_reservations_by_consumer", return_value=[]):
        with pytest.raises(HTTPException) as exc:
            consumer_service.check_streak(consumer_id=1, db=mock_db)
        assert exc.value.status_code == 404



# Each badge has a check function that examines the consumer's reservation history and awards the badge when the condition is met.
# These tests verify both the positive case (condition met = badge awarded) and the negative case (condition not met = no badge).


# 'Good Start' is awarded when the consumer's first reservation is collected.
def test_check_good_start_awards_badge(mock_db):
    
    mock_res = MagicMock()

    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=[mock_res]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_good_start(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Good Start", consumer_id=1, db=mock_db)


def test_check_good_start_no_reservations(mock_db):
    
    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=[]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_good_start(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

# 'First Rescue' is awarded when the consumer has at least one collected reservation.
def test_check_first_rescue_awards_badge(mock_db):
    
    mock_res = _mock_collected_reservation(days_ago=0)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[mock_res]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_first_rescue(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="First Rescue", consumer_id=1, db=mock_db)


def test_check_first_rescue_no_collections(mock_db):
    
    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_first_rescue(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

# 'On a Roll' is awarded when the consumer has collected reservations on 3 consecutive days.
def test_check_on_a_roll_3_consecutive_days(mock_db):
    
    res1 = _mock_collected_reservation(days_ago=0)
    res2 = _mock_collected_reservation(days_ago=1)
    res3 = _mock_collected_reservation(days_ago=2)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res1, res2, res3]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_on_a_roll(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="On a Roll", consumer_id=1, db=mock_db)


def test_check_on_a_roll_not_consecutive(mock_db):
    
    res1 = _mock_collected_reservation(days_ago=0)
    res2 = _mock_collected_reservation(days_ago=1)
    res3 = _mock_collected_reservation(days_ago=5)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res1, res2, res3]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_on_a_roll(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()


def test_check_on_a_roll_too_few(mock_db):
    
    res1 = _mock_collected_reservation(days_ago=0)
    res2 = _mock_collected_reservation(days_ago=1)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res1, res2]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_on_a_roll(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

# 'Locked In' is awarded for a 7-day streak.
def test_check_locked_in_7_consecutive_days(mock_db):
    
    reservations = [_mock_collected_reservation(days_ago=i) for i in range(7)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_locked_in(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Locked In", consumer_id=1, db=mock_db)


def test_check_locked_in_too_few(mock_db):
    
    reservations = [_mock_collected_reservation(days_ago=i) for i in range(5)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_locked_in(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

# 'Triple Threat' is awarded when the consumer collects 3 reservations in a single day.
def test_check_triple_threat_same_day(mock_db):
    
    res1 = _mock_collected_reservation(days_ago=0)
    res2 = _mock_collected_reservation(days_ago=0)
    res3 = _mock_collected_reservation(days_ago=0)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res1, res2, res3]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_triple_threat(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Triple Threat", consumer_id=1, db=mock_db)


def test_check_triple_threat_different_days(mock_db):
    
    res1 = _mock_collected_reservation(days_ago=0)
    res2 = _mock_collected_reservation(days_ago=1)
    res3 = _mock_collected_reservation(days_ago=2)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res1, res2, res3]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_triple_threat(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

# 'Waste Warrior' is awarded when the consumer has collected over 1 kg of waste across all reservations.
def test_check_waste_warrior_over_1kg(mock_db):
    
    res1 = _mock_collected_reservation(weight=600)
    res2 = _mock_collected_reservation(weight=500)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res1, res2]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_waste_warrior(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Waste Warrior", consumer_id=1, db=mock_db)


def test_check_waste_warrior_under_1kg(mock_db):
    
    res1 = _mock_collected_reservation(weight=400)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res1]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_waste_warrior(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

# 'Punctual' is awarded when the consumer has collected 10 reservations.
def test_check_punctual_10_collected(mock_db):
    
    reservations = [MagicMock(status=ReservationStatus.COLLECTED) for _ in range(10)]

    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_punctual(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with("Punctual", consumer_id=1, db=mock_db)


def test_check_punctual_not_all_collected(mock_db):
    
    reservations = [MagicMock(status=ReservationStatus.COLLECTED) for _ in range(9)]
    reservations.append(MagicMock(status=ReservationStatus.NO_SHOW))

    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_punctual(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

# 'Familiar Face' is awarded when the consumer has collected 3 reservations from the same place.
def test_check_familiar_face_awards_badge(mock_db):
    
    reservations = [_mock_collected_reservation() for _ in range(3)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.reservation.check_familiar_face", return_value=True), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_familiar_face(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Familiar Face", consumer_id=1, db=mock_db)


def test_check_familiar_face_not_enough(mock_db):
    
    reservations = [_mock_collected_reservation() for _ in range(2)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_familiar_face(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()

#'Well Rounded' is awarded when the consumer has collected reservations from at least 3 different categories.
def test_check_well_rounded_awards_badge(mock_db):
    
    with patch("app.crud.reservation.check_well_rounded", return_value=True), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_well_rounded(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Well Rounded", consumer_id=1, db=mock_db)


def test_check_well_rounded_not_all_categories(mock_db):
    
    with patch("app.crud.reservation.check_well_rounded", return_value=False), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_well_rounded(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()




def test_award_badge_skips_if_already_awarded(mock_db):
   # If the consumer already has the badge, award_badge should not insert a duplicate record.
    mock_badge = MagicMock()
    mock_badge.badge_id = 1
    mock_existing = MagicMock()

    mock_db.exec.return_value.first.side_effect = [mock_badge, mock_existing]

    badge_crud.award_badge(badge_name="First Rescue", consumer_id=1, db=mock_db)

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()


def test_award_badge_inserts_if_not_awarded(mock_db):
    # If the consumer does not already have the badge, award_badge should insert a new ConsumerBadge record.
    mock_badge = MagicMock()
    mock_badge.badge_id = 1

    mock_db.exec.return_value.first.side_effect = [mock_badge, None]

    badge_crud.award_badge(badge_name="First Rescue", consumer_id=1, db=mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_award_badge_skips_if_badge_not_found(mock_db):
    # If the badge name does not exist in the Badge table, award_badge should do nothing (not insert or commit).
    mock_db.exec.return_value.first.return_value = None

    badge_crud.award_badge(badge_name="NonExistentBadge", consumer_id=1, db=mock_db)

    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()



# 'Relentless' is awarded for 30 consecutive days of collections.

def test_check_relentless_awards_on_30_day_streak(mock_db):
   
    reservations = [_mock_collected_reservation(days_ago=i) for i in range(30)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_relentless(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Relentless", consumer_id=1, db=mock_db)


def test_check_relentless_skips_when_fewer_than_30(mock_db):
   
    reservations = [_mock_collected_reservation(days_ago=i) for i in range(20)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_relentless(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()


# 'Eco Advocate' is awarded when the consumer has collected over 10 kg of waste across all reservations.

def test_check_eco_advocate_awards_over_10kg(mock_db):
    
    # 2 × 5 500 g = 11 000 g  (> 10 000 g threshold)
    reservations = [_mock_collected_reservation(weight=5500) for _ in range(2)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_eco_advocate(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Eco Advocate", consumer_id=1, db=mock_db)


def test_check_eco_advocate_skips_under_10kg(mock_db):
    """
    Total weight 8 000 g (< 10 000 g) → badge is not awarded.
    """
    reservations = [_mock_collected_reservation(weight=4000) for _ in range(2)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_eco_advocate(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()


# 'Green Guardian' is awarded when the consumer has collected over 25 kg of waste across all reservations.

def test_check_green_guardian_awards_over_25kg(mock_db):
    
    
    reservations = [_mock_collected_reservation(weight=13000) for _ in range(2)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_green_guardian(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Green Guardian", consumer_id=1, db=mock_db)


def test_check_green_guardian_skips_under_25kg(mock_db):
    
    reservations = [_mock_collected_reservation(weight=10000) for _ in range(2)]

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_green_guardian(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()


# 'Timekeeper' is awarded when all of the last 25 reservations have status COLLECTED .

def test_check_timekeeper_awards_on_25_collected(mock_db):
    
    reservations = [MagicMock(status=ReservationStatus.COLLECTED) for _ in range(25)]

    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_timekeeper(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with("Timekeeper", consumer_id=1, db=mock_db)


def test_check_timekeeper_skips_fewer_than_25(mock_db):
    
    reservations = [MagicMock(status=ReservationStatus.COLLECTED) for _ in range(20)]

    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_timekeeper(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()


# 'Unshakeable' is awarded when all of the last 50 reservations have status COLLECTED — the highest reliability tier.

def test_check_unshakeable_awards_on_50_collected(mock_db):
    
    reservations = [MagicMock(status=ReservationStatus.COLLECTED) for _ in range(50)]

    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_unshakeable(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with("Unshakeable", consumer_id=1, db=mock_db)


def test_check_unshakeable_fails_with_no_show(mock_db):
    
    reservations = [MagicMock(status=ReservationStatus.COLLECTED) for _ in range(49)]
    reservations.append(MagicMock(status=ReservationStatus.NO_SHOW))

    with patch("app.crud.reservation.get_reservations_by_consumer", return_value=reservations), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_unshakeable(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()


# 'Final Call' is awarded when a collection happened within 5 minutes of the pickup window closing.

def test_check_final_call_awards_within_5_minutes(mock_db):
    
    now = datetime.now(timezone.utc)
    res = _mock_collected_reservation(days_ago=0)
    res.posting.pickup_window = MagicMock()
    
    res.posting.pickup_window.upper = now + timedelta(minutes=3)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_final_call(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Final Call", consumer_id=1, db=mock_db)


def test_check_final_call_skips_when_not_close(mock_db):
    
    now = datetime.now(timezone.utc)
    res = _mock_collected_reservation(days_ago=0)
    res.posting.pickup_window = MagicMock()
    
    res.posting.pickup_window.upper = now + timedelta(hours=1)

    with patch("app.crud.reservation.get_consumers_collected_reservations", return_value=[res]), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_final_call(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()


# 'Weatherproof' is awarded when the consumer has 5+ records with raining=True.

def test_check_weatherproof_awards_on_5_rainy(mock_db):
   
    records = [MagicMock(raining=True) for _ in range(5)]

    with patch("app.crud.record.get_records_by_consumer", return_value=records), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_weatherproof(consumer_id=1, db=mock_db)
        mock_award.assert_called_once_with(badge_name="Weatherproof", consumer_id=1, db=mock_db)


def test_check_weatherproof_skips_under_5_rainy(mock_db):
    
    records = [MagicMock(raining=True) for _ in range(3)]
    records.append(MagicMock(raining=False))

    with patch("app.crud.record.get_records_by_consumer", return_value=records), \
         patch("app.crud.badge.award_badge") as mock_award:
        badge_service.check_weatherproof(consumer_id=1, db=mock_db)
        mock_award.assert_not_called()
