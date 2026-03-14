from decimal import Decimal
from sqlmodel import Session, select, func
from psycopg2.extras import DateTimeTZRange
from app.db.session import engine
from app.core.security import get_password_hash
from datetime import datetime, timedelta, timezone
from app.db.base import BundlePosting, Consumer, Forecast, Record, Reservation, Seller, User
from app.models.enums import Role, ReservationStatus, BundleStatus, Category
from random import choices
from faker import Faker
import numpy as np

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

    #Add 250 users with consumer role
    for _ in range(250):
        password = fake.password(length=8, special_chars=False, digits=True, upper_case=False, lower_case=True)
        user = User(
            role=Role.CONSUMER,
            email=fake.email(),
            password=get_password_hash(password)
            )
        db.add(user)

    #Add 250 users with seller role
    for _ in range(250):
        password = fake.password(length=8, special_chars=False, digits=True, upper_case=False, lower_case=True)
        user = User(
            role=Role.SELLER,
            email=fake.email(),
            password=get_password_hash(password)
            )
        db.add(user)

    #Add 10 users with admin role
    for _ in range(10): 
        password=get_password_hash(password)
        user = User(
            role=Role.ADMIN,
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
            display_name=fake.name()
        )
        db.add(consumer)
    db.commit()

def seed_seller(db: Session):
    #Get all the seller
    sellers = db.exec(select(User).where(User.role == Role.SELLER)).all()

    #Add users with the seller role to the seller table
    for user in sellers:
        #Create random opening hours
        opening_time = fake.random_int(8, 11)
        closing_time = fake.random_int(16, 20)
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
        reservations = fake.random_int(1, 25)

        #Create random 1 hour pickup window
        day = 1 + calculate_day_of_week(reservations) + (fake.random_int(0, 3) * 7)
        start_time = datetime(2026, 3, day, calculate_start_time(reservations), tzinfo=timezone.utc)
        end_time = start_time + timedelta(hours=1)
        pickup_window = DateTimeTZRange(start_time, end_time, bounds='[)')

        #Randomise status based on pickup window
        if pickup_window.upper != None:
            if datetime.now(timezone.utc) > pickup_window.upper:
                status = BundleStatus.EXPIRED
            else:
                status = fake.random_element(elements=[BundleStatus.AVAILABLE, BundleStatus.SOLD_OUT])

        #Assign each post to a random seller
        posting = BundlePosting(
            user_id=fake.random_element(elements=sellers).user_id,
            category=calculate_category(reservations),
            allergens=', '.join(fake.random_elements(elements=example_allergens, unique=True)),
            available=fake.random_int(0, 5),
            reserved=reservations,
            price=Decimal(calculate_price(reservations)),
            pickup_window=pickup_window,
            status=status,
            weight=fake.random_int(250, 2000)
        )
        db.add(posting)
    db.commit()

def seed_reservation(db: Session):
    #Get all the consumers and posts
    consumers = db.exec(select(Consumer)).all()
    postings = db.exec(select(BundlePosting)).all()

    #Create 1-25 reservations for each bundle posting and assign each one to a random consumer
    for post in postings:
        for _ in range(post.reserved):
            #Randomise timestamp based on post pickup window
            if post.pickup_window.lower < datetime.now(timezone.utc):
                timestamp = post.pickup_window.lower - timedelta(days=fake.random_int(0, 3), hours=fake.random_int(1, 23))
            else:
                timestamp = datetime.now(timezone.utc) - timedelta(days=fake.random_int(0, 3), hours=fake.random_int(1, 23))

            #Randomise status based on post status
            if post.status == BundleStatus.EXPIRED:
                status = fake.random_element(elements=[ReservationStatus.COLLECTED, ReservationStatus.NO_SHOW])
            else:
                status = ReservationStatus.RESERVED

            reservation = Reservation(
                posting_id=post.posting_id,
                user_id=fake.random_element(elements=consumers).user_id,
                timestamp=timestamp,
                status=status
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

        reservations = post.available - post.reserved

        record = Record(
            user_id=post.user_id,
            posting_id=post.posting_id,
            pickup_window=post.pickup_window,
            category=post.category,
            price=post.price,
            raining=calculate_rain(reservations),
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
            predicted_reservations=fake.random_int(5, 50),
            predicted_no_show_prob=round(fake.pyfloat(min_value=0, max_value=0.25), 2)
        )
        db.add(forecast)
    db.commit()

#Price based on number of reservations
def calculate_price(reservations: int) -> float:
    base_price = (250/reservations) ** (2/3)
    random_noise = np.random.normal(0, 0.2)
    price = base_price * np.exp(random_noise)

    return round(price, 2)

#Start time based on number of reservations
def calculate_start_time(reservations: int) -> int:
    peak_prob = 0.4 + (0.02 * reservations)
    is_peak = np.random.random() < peak_prob

    if is_peak:
        if np.random.random() < 0.5:
            time = np.random.normal(12.5, 1)
        else:
            time = np.random.normal(17.5, 0.8**2)
    else:
        time = fake.random_int(8, 18)

    return int(time)

#Day of the week based on number of reservations
def calculate_day_of_week(reservations: int) -> int:
    b = 0.02 * (reservations - 12.5)
    w = 0.4 + b
    d = 1 - w
    k = d/0.6

    #Monday - Sunday
    day_probs = {
        1: 0.1 * k, 
        2: 0.1 * k,
        3: 0.12 * k,
        4: 0.12 * k,
        5: w * 0.18 / 0.4,
        6: w * 0.22 / 0.4,
        7: 0.16 * k
    }

    days = list(day_probs.keys())
    probs = list(day_probs.values())

    return np.random.choice(a=days, p=probs)

#Category based on number of reservations
def calculate_category(reservations: int) -> Category:
    b = 0.015 * (reservations - 12.5)
    h = 0.55 + b
    o = 1 - h
    k = o/0.45

    category_probs = {
        Category.MEAT: 0.14 * k, 
        Category.DAIRY: 0.11 * k,
        Category.FRUIT: 0.09 * k,
        Category.VEGETABLES: 0.07 * k,
        Category.SEAFOOD: 0.04 * k,
        Category.BAKED_GOODS: h * 0.22 / 0.55,
        Category.SNACKS: h * 0.18 / 0.55,
        Category.DRINKS: h * 0.15 / 0.55
    }

    categories = list(category_probs.keys())
    probs = list(category_probs.values())

    return choices(categories, weights=probs, k=1)[0]

#Rain based on number of reservations
def calculate_rain(reservations: int) -> bool:
    b = 0.01 * (reservations - 12.5)

    return np.random.random() < 0.3 - b

#Update streaks for all users based on number of weeks they have collected a bundle
def update_streaks(db: Session):
    consumers = db.exec(select(Consumer)).all()

    for consumer in consumers:
        reservations = list(db.exec(select(Reservation).where(
            Reservation.user_id == consumer.user_id,
            Reservation.status == ReservationStatus.COLLECTED
        )).all())

        streak = 0
        week_end = datetime.now(timezone.utc)
        
        while True:
            week_start = week_end - timedelta(weeks=1)
            has_collection = any(week_start <= r.timestamp < week_end for r in reservations)
            if has_collection:
                streak += 1
                week_end = week_start
            else:
                break
        
        consumer.streak = streak
        db.add(consumer)

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
        update_streaks(db=db)
        seed_record(db=db)
        seed_forecast(db=db)
    print("Seeding complete")

if __name__ == "__main__":
    seed_tables()