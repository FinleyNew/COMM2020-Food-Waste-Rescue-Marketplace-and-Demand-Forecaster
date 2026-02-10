from decimal import Decimal
from sqlmodel import Session, select, func
from psycopg2.extras import DateTimeTZRange
from app.db.session import engine
from datetime import datetime, timedelta
from app.db.base import BundlePosting, Consumer, Forecast, Record, Reservation, Seller, User
from app.models.enums import Role, ReservationStatus, BundleStatus, Category
from random import randint, uniform
from faker import Faker

fake = Faker('en_GB')
Faker.seed(123)

def is_database_already_seeded(db: Session):
    #Check if any users exist
    statement = select(func.count()).select_from(User)
    user_count = db.exec(statement).one()
    return user_count > 0

def seed_users(db: Session):
    for _ in range(100):
        role = fake.random_element(elements=Role).value
        user = User(
            role=role
            )
        db.add(user)
    db.commit()

def seed_consumer(db: Session):
    consumers = db.exec(select(User).where(User.role == Role.CONSUMER)).all()
    
    for user in consumers:
        consumer = Consumer(
            user_id=user.user_id,
            display_name=fake.name(),
            streak=fake.random_int(0, 10)
        )
        db.add(consumer)
    db.commit()

def seed_seller(db: Session):
    sellers = db.exec(select(User).where(User.role == Role.SELLER)).all()

    for user in sellers:
        opening_time = randint(8, 11)
        closing_time = randint(16, 20)
        opening_hours = f"{opening_time}:00 - {closing_time}:00"

        seller = Seller(
            user_id=user.user_id,
            name=fake.company(),
            location=fake.address(),
            opening_hours=opening_hours
        )
        db.add(seller)
    db.commit()

def seed_bundle_posting(db: Session):
    sellers = db.exec(select(Seller)).all()
    example_allergens = ['Milk', 'Eggs', 'Nuts', 'Shellfish', 'Gluten', 'Soy', 'Wheat', 'Fish', 'Sesame', 'Celery']

    for _ in range(250):
        start_time = datetime(2026, randint(1,2), randint(1, 28), randint(9, 17))
        end_time = start_time + timedelta(hours=2)
        pickup_window = DateTimeTZRange(start_time, end_time, bounds='[)')

        posting = BundlePosting(
            user_id=fake.random_element(elements=sellers).user_id,
            category=fake.random_element(elements=Category).value,
            allergens=', '.join(fake.random_elements(elements=example_allergens, unique=True)),
            available=randint(0, 25),
            reserved=randint(0, 25),
            price=Decimal(uniform(5.0, 15.0)),
            pickup_window=pickup_window,
            status=fake.random_element(elements=BundleStatus).value
        )
        db.add(posting)
    db.commit()


def seed_reservation(db: Session):
    consumers = db.exec(select(Consumer)).all()
    postings = db.exec(select(BundlePosting)).all()

    for _ in range(400):
        reservation = Reservation(
            posting_id=fake.random_element(elements=postings).posting_id,
            user_id=fake.random_element(elements=consumers).user_id,
            timestamp=fake.date_time_between(datetime(2026, 1, 1), datetime(2026, 2, 10)),
            status=fake.random_element(elements=ReservationStatus).value
        )
        db.add(reservation)
    db.commit()

def seed_record(db: Session):
    postings = db.exec(select(BundlePosting).where(BundlePosting.status == BundleStatus.EXPIRED)).all()

    for post in postings:
        reservations_query = select(func.count()).select_from(Reservation).where(
            Reservation.posting_id == post.posting_id,
            Reservation.status.in_([ReservationStatus.COLLECTED, ReservationStatus.NO_SHOW])
        )
        reservations = db.exec(reservations_query).one()

        no_show_query = select(func.count()).select_from(Reservation).where(
            Reservation.posting_id == post.posting_id,
            Reservation.status == ReservationStatus.NO_SHOW
        )
        no_show = db.exec(no_show_query).one()

        record = Record(
            user_id=post.user_id,
            posting_id=post.posting_id,
            pickup_window=post.pickup_window,
            category=post.category,
            price=post.price,
            raining=fake.boolean(chance_of_getting_true=10),
            observed_reservations=reservations,
            observed_no_show=no_show
        )
        db.add(record)
    db.commit()

def seed_forecast(db: Session):
    postings = db.exec(select(BundlePosting).where(BundlePosting.status == BundleStatus.AVAILABLE)).all()

    for i in range(3):
        post = postings[i]

        forecast = Forecast(
            user_id=post.user_id,
            posting_id=post.posting_id,
            predicted_reservations=randint(5, 50),
            predicted_no_show_prob=uniform(0, 0.25)
        )
        db.add(forecast)
    db.commit()


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
        seed_record(db=db)
        seed_forecast(db=db)
    print("Seeding complete")

if __name__ == "__main__":
    seed_tables()