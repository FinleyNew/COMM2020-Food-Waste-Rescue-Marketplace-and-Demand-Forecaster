from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from sqlmodel import Session

from app.crud.bundlePosting import get_to_be_expired_bundle_postings, set_expired, get_to_be_emailed_bundle_postings
from app.db.session import engine
from app.models.enums import ReservationStatus
from app.crud.reservation import set_no_show
from app.services import record as record_service
from app.services import email as email_service
from app.core.config import settings

scheduler = AsyncIOScheduler()

# This function adds jobs to the scheduler and starts it
def start_scheduler():
    # Adds job to check for expired postings every minute
    scheduler.add_job(
        check_expired_postings,
        IntervalTrigger(minutes=1),
    )
    # Adds the job to send emails to users but only if the API key is available
    if settings.SENDGRID_API_KEY != "":
        scheduler.add_job(
            email_notifications,
            IntervalTrigger(minutes=1)
        )
    scheduler.start()

# This function stops the scheduler
def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)

# This is the job for checking expired postings
async def check_expired_postings():
    with Session(engine) as db:
        # Gets the current date and time
        now = datetime.now(timezone.utc)

        # Gets all postings from the DB that have passed there collection window
        expired = get_to_be_expired_bundle_postings(now=now, db=db)
        # Loops through these postings setting each one to expired and creating a record
        for posting in expired:
            set_expired(bundle_posting=posting, db=db)
            record_service.create_record(bundle_posting=posting, db=db)
            reservations = posting.reservations
            # Loops through the related reservations and sets any that are still reserved to no_show
            for reservation in reservations:
                if reservation.status == ReservationStatus.RESERVED:
                    set_no_show(reservation=reservation, db=db)
        
        db.commit()

# This is the job for sending out email notifications
async def email_notifications():
    with Session(engine) as db:
        # Gets the current time
        now = datetime.now(timezone.utc)
        # Gets the bundles that need to be emailed
        emails = get_to_be_emailed_bundle_postings(now=now, db=db)
        # Goes through each of the reservations for this posting sending an email to each one
        for posting in emails:
            for reservation in posting.reservations:
                email = reservation.consumer.user.email
                email_service.send_email(to_email=email, subject="Your reservation", body="Just a reminder you have a reservation and collection starts in 30 minuites")

