from datetime import datetime, timedelta, timezone
from typing import Sequence

from sqlmodel import Session
from app.crud import badge as badge_crud
from app.crud import reservation as reservation_crud
from app.crud import record as record_crud
from app.models.enums import ReservationStatus
from app.models.badge import Badge

def get_all_badges(db: Session) -> Sequence[Badge]:
    return badge_crud.get_all_badges(db=db)

def check_at_reservation(consumer_id: int, db: Session):
    check_good_start(consumer_id=consumer_id, db=db)

def check_at_collection(consumer_id: int, db: Session):
    check_first_rescue(consumer_id=consumer_id, db=db)
    check_on_a_roll(consumer_id=consumer_id, db=db)
    check_locked_in(consumer_id=consumer_id, db=db)
    check_relentless(consumer_id=consumer_id, db=db)
    check_waste_warrior(consumer_id=consumer_id, db=db)
    check_eco_advocate(consumer_id=consumer_id, db=db)
    check_green_guardian(consumer_id=consumer_id, db=db)
    check_punctual(consumer_id=consumer_id, db=db)
    check_timekeeper(consumer_id=consumer_id, db=db)
    check_unshakeable(consumer_id=consumer_id, db=db)
    check_final_call(consumer_id=consumer_id, db=db)
    check_weatherproof(consumer_id=consumer_id, db=db)
    check_triple_threat(consumer_id=consumer_id, db=db)
    check_familiar_face(consumer_id=consumer_id, db=db)
    check_well_rounded(consumer_id=consumer_id, db=db)

def check_good_start(consumer_id: int, db: Session):
    # Award if that consumer has at least one reservation
    if reservation_crud.get_reservations_by_consumer(consumer_id=consumer_id, db=db):
        badge_crud.award_badge(badge_name="Good Start", consumer_id=consumer_id, db=db)

def check_first_rescue(consumer_id: int, db: Session):
    # Award if this consumer has at least one collected reservation
    if reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db):
        badge_crud.award_badge(badge_name="First Rescue", consumer_id=consumer_id, db=db)

def check_on_a_roll(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    if len(reservations) < 3:
        return
    last_3 = reservations[:3]
    # Get the dates from the last 3 reservations
    dates = [r.timestamp.date() for r in last_3]
    # Check if these dates are a streak
    is_streak = all(
        dates[i] - dates[i+1] == timedelta(days=1)
        for i in range(len(dates) - 1)
    )
    if is_streak:
        badge_crud.award_badge(badge_name="On a Roll", consumer_id=consumer_id, db=db)

def check_locked_in(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    if len(reservations) < 7:
        return
    last_7 = reservations[:7]
    # Get the dates from the last 7 reservations
    dates = [r.timestamp.date() for r in last_7]
    # Check if these dates are a streak
    is_streak = all(
        dates[i] - dates[i+1] == timedelta(days=1)
        for i in range(len(dates) - 1)
    )
    if is_streak:
        badge_crud.award_badge(badge_name="Locked In", consumer_id=consumer_id, db=db)

def check_relentless(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    if len(reservations) < 30:
        return
    last_30 = reservations[:30]
    # Get the dates from the last 30 reservations
    dates = [r.timestamp.date() for r in last_30]
    # Check if these dates are a streak
    is_streak = all(
        dates[i] - dates[i+1] == timedelta(days=1)
        for i in range(len(dates) - 1)
    )
    if is_streak:
        badge_crud.award_badge(badge_name="Relentless", consumer_id=consumer_id, db=db)

def check_waste_warrior(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    # Get the total weight of all the consumers bundles
    weight = sum(r.posting.weight for r in reservations)
    # If its greater than one kg award the badge
    if weight >= 1000:
        badge_crud.award_badge(badge_name="Waste Warrior", consumer_id=consumer_id, db=db)

def check_eco_advocate(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    # Get the total weight of all the consumers bundles
    weight = sum(r.posting.weight for r in reservations)
    # If its greater than ten kgs award the badge
    if weight >= 10000:
        badge_crud.award_badge(badge_name="Eco Advocate", consumer_id=consumer_id, db=db)

def check_green_guardian(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    # Get the total weight of all the consumers bundles
    weight = sum(r.posting.weight for r in reservations)
    # If its greater than twenty five kgs award the badge
    if weight >= 25000:
        badge_crud.award_badge(badge_name="Green Guardian", consumer_id=consumer_id, db=db)

def check_punctual(consumer_id: int, db: Session):
    reservations = reservation_crud.get_reservations_by_consumer(consumer_id=consumer_id, db=db)
    if len(reservations) < 10:
        return
    last_10 = reservations[:10]
    all_collected = all(
        r.status == ReservationStatus.COLLECTED
        for r in last_10
    )
    if all_collected:
        badge_crud.award_badge("Punctual", consumer_id=consumer_id, db=db)

def check_timekeeper(consumer_id: int, db: Session):
    reservations = reservation_crud.get_reservations_by_consumer(consumer_id=consumer_id, db=db)
    if len(reservations) < 25:
        return
    last_25 = reservations[:25]
    all_collected = all(
        r.status == ReservationStatus.COLLECTED
        for r in last_25
    )
    if all_collected:
        badge_crud.award_badge("Timekeeper", consumer_id=consumer_id, db=db)

def check_unshakeable(consumer_id: int, db: Session):
    reservations = reservation_crud.get_reservations_by_consumer(consumer_id=consumer_id, db=db)
    if len(reservations) < 50:
        return
    last_50 = reservations[:50]
    all_collected = all(
        r.status == ReservationStatus.COLLECTED
        for r in last_50
    )
    if all_collected:
        badge_crud.award_badge("Unshakeable", consumer_id=consumer_id, db=db)

def check_final_call(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    if not reservations:
        return
    reservation = reservations[0]
    now = datetime.now(timezone.utc)
    pickup_end = reservation.posting.pickup_window.upper
    time_until_end = pickup_end - now
    if timedelta(0) <= time_until_end <= timedelta(minutes=5):
        badge_crud.award_badge(badge_name="Final Call", consumer_id=consumer_id, db=db)

def check_weatherproof(consumer_id: int, db: Session):
    records = record_crud.get_records_by_consumer(consumer_id=consumer_id, db=db)
    if not records:
        return
    raining_count = sum(1 for r in records if r.raining)
    if raining_count >= 5:
        badge_crud.award_badge(badge_name="Weatherproof", consumer_id=consumer_id, db=db)
    

def check_triple_threat(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    if len(reservations) < 3:
        return
    last_3 = reservations[:3]
    dates = [r.timestamp.date() for r in last_3]
    if len(set(dates)) == 1:
        badge_crud.award_badge(badge_name="Triple Threat", consumer_id=consumer_id, db=db)

def check_familiar_face(consumer_id: int, db: Session):
    reservations = reservation_crud.get_consumers_collected_reservations(consumer_id=consumer_id, db=db)
    if len(reservations) < 3:
        return
    if reservation_crud.check_familiar_face(consumer_id=consumer_id, db=db):
        badge_crud.award_badge(badge_name="Familiar Face", consumer_id=consumer_id, db=db)

def check_well_rounded(consumer_id: int, db: Session):
    if reservation_crud.check_well_rounded(consumer_id=consumer_id, db=db):
        badge_crud.award_badge(badge_name="Well Rounded", consumer_id=consumer_id, db=db)