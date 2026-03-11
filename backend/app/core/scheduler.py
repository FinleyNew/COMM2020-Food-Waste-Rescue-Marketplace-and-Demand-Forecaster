from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from sqlmodel import Session

from app.crud.bundlePosting import get_to_be_expired_bundle_postings, set_expired
from app.db.session import engine
from app.models.enums import ReservationStatus
from app.crud.reservation import set_no_show

scheduler = AsyncIOScheduler()

def start_scheduler():
    scheduler.add_job(
        check_expired_postings,
        IntervalTrigger(minutes=1),
    )
    scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)

async def check_expired_postings():
    with Session(engine) as db:
        now = datetime.now(timezone.utc)

        expired = get_to_be_expired_bundle_postings(now=now, db=db)
        for posting in expired:
            set_expired(bundle_posting=posting, db=db)
            reservations = posting.reservations
            for reservation in reservations:
                if reservation.status == ReservationStatus.RESERVED:
                    set_no_show(reservation=reservation, db=db)
        
        db.commit()