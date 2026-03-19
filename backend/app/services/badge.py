from sqlmodel import Session

from app.crud import badge as badge_crud
from app.crud import reservation as reservation_crud

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
    pass

def check_on_a_roll(consumer_id: int, db: Session):
    pass

def check_locked_in(consumer_id: int, db: Session):
    pass

def check_relentless(consumer_id: int, db: Session):
    pass

def check_waste_warrior(consumer_id: int, db: Session):
    pass

def check_eco_advocate(consumer_id: int, db: Session):
    pass

def check_green_guardian(consumer_id: int, db: Session):
    pass

def check_punctual(consumer_id: int, db: Session):
    pass

def check_timekeeper(consumer_id: int, db: Session):
    pass

def check_unshakeable(consumer_id: int, db: Session):
    pass

def check_final_call(consumer_id: int, db: Session):
    pass

def check_weatherproof(consumer_id: int, db: Session):
    pass

def check_triple_threat(consumer_id: int, db: Session):
    pass

def check_familiar_face(consumer_id: int, db: Session):
    pass

def check_well_rounded(consumer_id: int, db: Session):
    pass