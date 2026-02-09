from decimal import Decimal
from sqlmodel import Session, select, func
from psycopg2.extras import DateTimeTZRange
from app.db.session import engine
from datetime import datetime, timezone, timedelta
from app.db.base import BundlePosting, Consumer, Forecast, Record, Reservation, Seller, User
from app.models.enums import Role, ReservationStatus, BundleStatus, Category

def is_database_already_seeded(db: Session):
    #Check if any users exist
    statement = select(func.count()).select_from(User)
    user_count = db.exec(statement).one()
    return user_count > 0

def seed_users(db: Session):
    test_consumer_user = User(user_id=1, role=Role.CONSUMER)
    test_seller_user = User(user_id=2, role=Role.SELLER)
    db.add(test_consumer_user)
    db.add(test_seller_user)
    db.commit()

def seed_consumer(db: Session):
    test_consumer = Consumer(user_id=2, display_name="TopConsumer")

def seed_seller(db: Session):
    test_seller = Seller(user_id=2, name="TopSeller", location="Test, Address", opening_hours="11:00 - 21:00")
    db.add(test_seller)
    db.commit()

def seed_bundle_posting(db: Session):
    start_time = datetime(2026, 2, 15, 14, tzinfo=timezone.utc)
    end_time = start_time + timedelta(hours=2)
    pickup_window = DateTimeTZRange(start_time, end_time, bounds='[)')
    test_bundle_posting = BundlePosting(posting_id=1, user_id=2, category=Category.BAKED_GOODS, allergens="TestAllergens", available=10, price=Decimal(4.50), pickup_window=pickup_window)
    db.add(test_bundle_posting)
    db.commit()

def seed_reservation(db: Session):
    test_reservation = Reservation(reservation_id=1, posting_id=1, user_id=2)

#def seed_record(db: Session):

#def seed_forecast(db: Session):

def seed_tables():
    with Session(engine) as db:
        if is_database_already_seeded(db=db):
            print("DB already seeded")
            return
        print("Seeding data")
        seed_users(db=db)
        seed_consumer(db=db)
        seed_seller(db=db)
        seed_bundle_posting(db=db)
        seed_reservation(db=db)
    print("Seeding complete")

if __name__ == "__main__":
    seed_tables()