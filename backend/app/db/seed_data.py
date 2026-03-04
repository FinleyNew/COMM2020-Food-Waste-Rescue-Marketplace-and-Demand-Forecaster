from decimal import Decimal
from sqlmodel import Session, select, func
from psycopg2.extras import DateTimeTZRange
from app.db.session import engine
from app.core.security import get_password_hash
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
    #Hardcode first 2 users as consumer and seller
    consumer_user = User(
        role=Role.CONSUMER,
        email="consumer@gmail.com",
        password=get_password_hash("123"))
    seller_user = User(
        role=Role.SELLER,
        email="seller@gmail.com",
        password=get_password_hash("123"))
    db.add(consumer_user)
    db.add(seller_user)

    #Add 100 users with a random role
    for _ in range(100):
        role = fake.random_element(elements=Role).value
        password = fake.password(length=8, special_chars=False, digits=True, upper_case=False, lower_case=True)
        user = User(
            role=role,
            email=fake.email(),
            password=get_password_hash(password)
            )
        db.add(user)
    db.commit()

def seed_consumer(db: Session):
    #Get all the users with consumer role
    consumers = db.exec(select(User).where(User.role == Role.CONSUMER)).all()
    
    #Add users with the consumer role to the consumer table
    for user in consumers:
        #Give consumer random and and streak between 1 and 10
        consumer = Consumer(
            user_id=user.user_id,
            display_name=fake.name(),
            streak=fake.random_int(0, 10)
        )
        db.add(consumer)
    db.commit()

def seed_seller(db: Session):
    #Get all the seller
    sellers = db.exec(select(User).where(User.role == Role.SELLER)).all()

    #Add users with the seller role to the seller table
    for user in sellers:
        #Create random opening hours
        opening_time = randint(8, 11)
        closing_time = randint(16, 20)
        opening_hours = f"{opening_time}:00 - {closing_time}:00"

        #Give seller fake name and address
        seller = Seller(
            user_id=user.user_id,
            name=fake.company(),
            location=fake.address(),
            opening_hours=opening_hours
        )
        db.add(seller)
    db.commit()

def seed_bundle_posting(db: Session):
    #Get all the sellers
    sellers = db.exec(select(Seller)).all()
    example_allergens = ['Milk', 'Eggs', 'Nuts', 'Shellfish', 'Gluten', 'Soy', 'Wheat', 'Fish', 'Sesame', 'Celery']

    #Add 250 bundle postings
    for _ in range(250):
        #Create random 1 hour pickup window
        start_time = datetime(2026, randint(1,2), randint(1, 28), randint(8, 18))
        end_time = start_time + timedelta(hours=1)
        pickup_window = DateTimeTZRange(start_time, end_time, bounds='[)')

        #Assign each post to a random seller
        posting = BundlePosting(
            user_id=fake.random_element(elements=sellers).user_id,
            category=fake.random_element(elements=Category).value,
            allergens=', '.join(fake.random_elements(elements=example_allergens, unique=True)),
            available=randint(0, 25),
            reserved=randint(0, 25),
            price=Decimal(uniform(5.0, 15.0)),
            pickup_window=pickup_window,
            status=fake.random_element(elements=BundleStatus).value,
            weight=randint(250, 2000)
        )
        db.add(posting)
    db.commit()


def seed_reservation(db: Session):
    #Get all the consumers and posts
    consumers = db.exec(select(Consumer)).all()
    postings = db.exec(select(BundlePosting)).all()

    #Add 400 reservations
    for _ in range(400):
        #Assign each reservation to a random consumer and posting
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

    #Create record for every expired post
    for post in postings:
        #Get total number of reservations for the post
        reservations_query = select(func.count()).select_from(Reservation).where(
            Reservation.posting_id == post.posting_id
        )
        reservations = db.exec(reservations_query).one()

        #Get total number of no shows for the post
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
            observed_no_show=no_show,
            observed_expired=post.available,
            weight=post.weight
        )
        db.add(record)
    db.commit()

def seed_forecast(db: Session):
    postings = db.exec(select(BundlePosting).where(BundlePosting.status == BundleStatus.AVAILABLE)).all()

    #Create 3 forecasts with random values
    for i in range(3):
        post = postings[i]

        forecast = Forecast(
            user_id=post.user_id,
            posting_id=post.posting_id,
            predicted_reservations=randint(5, 50),
            predicted_no_show_prob=round(uniform(0, 0.25), 2)
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