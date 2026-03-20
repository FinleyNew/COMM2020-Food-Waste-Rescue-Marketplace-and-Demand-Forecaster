from decimal import Decimal
from sqlmodel import Session, select, func
from psycopg2.extras import DateTimeTZRange
from app.db.session import engine
from app.core.security import get_password_hash
from app.models.enums import Role, ReservationStatus, BundleStatus, Category, ReportStatus
from app.services.forecast import get_forecast
from datetime import datetime, timedelta, timezone
from app.db.base import BundlePosting, Consumer, Forecast, Record, Reservation, Seller, User, IssueReport
from random import choices
from app.models.badge import Badge
from faker import Faker
import numpy as np
from app.schemas.bundlePosting import BundlePostingCreate
from app.services.seller import get_coordinates

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
    admin_user = User(
        role=Role.ADMIN,
        email="admin@gmail.com",
        password=get_password_hash("123"))
    
    db.add(consumer_user)
    db.add(seller_user)
    db.add(admin_user)

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
        password = fake.password(length=8, special_chars=False, digits=True, upper_case=False, lower_case=True)
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
        latitude: float = 50.725545
        longitude: float = -3.526961

        #Give seller fake name and address
        seller = Seller(
            user_id=user.user_id,
            name=fake.company(),
            location=fake.address(),
            latitude=latitude,
            longitude=longitude,
            opening_hours=opening_hours
        )
        db.add(seller)
    db.commit()

def seed_bundle_posting(db: Session):
    #Get all the sellers
    sellers = db.exec(select(Seller)).all()

    example_allergens = {
        Category.BAKED_GOODS: ['Milk', 'Eggs', 'Wheat', 'Gluten', 'Soy'],
        Category.FRUIT: [],
        Category.VEGETABLES: ['Celery'],
        Category.MEAT: [],
        Category.SEAFOOD: ['Shellfish', 'Fish'],
        Category.SNACKS: ['Milk', 'Eggs', 'Nuts', 'Sesame'],
        Category.DAIRY: ['Milk', 'Soy'],
        Category.DRINKS: ['Milk']
    }

    #Add 250 bundle postings
    for _ in range(250):
        reservations = fake.random_int(1, 25)
        available = fake.random_int(0, 5)

        category = calculate_category(reservations)
        try:
            allergens = ', '.join(fake.random_elements(elements=example_allergens[category], unique=True))
        except:
            allergens = None

        #Create random 1 hour pickup window
        day = 1 + calculate_day_of_week(reservations) + (fake.random_int(0, 3) * 7)
        start_time = datetime(2026, 3, day, calculate_start_time(reservations), tzinfo=timezone.utc)
        end_time = start_time + timedelta(hours=1)
        pickup_window = DateTimeTZRange(start_time, end_time, bounds='[)')

        #Randomise status based on pickup window
        if pickup_window.upper != None:
            if datetime.now(timezone.utc) > pickup_window.upper:
                status = BundleStatus.EXPIRED
            elif available == 0:
                status = BundleStatus.SOLD_OUT
            else:    
                status = BundleStatus.AVAILABLE

        #Assign each post to a random seller
        posting = BundlePosting(
            user_id=fake.random_element(elements=sellers).user_id,
            category=category,
            allergens=allergens,
            available=available,
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

        record = Record(
            user_id=post.user_id,
            posting_id=post.posting_id,
            pickup_window=post.pickup_window,
            category=post.category,
            price=post.price,
            raining=calculate_rain(reservations),
            observed_reservations=post.reserved,
            observed_no_show=no_show,
            observed_expired=post.available,
            weight=post.weight
        )
        db.add(record)
    db.commit()

def seed_forecast(db: Session):
    postings = db.exec(select(BundlePosting)).all()

    #Create forecasts for all postings
    for post in postings:
        bundle_in = BundlePostingCreate(
            user_id=post.user_id or 0,
            category=post.category,
            allergens=post.allergens or "",
            available=max(1, post.available),
            price=post.price,
            weight=post.weight,
            start_time=post.pickup_window.lower,
            end_time=post.pickup_window.upper
        )
        forecast_data = get_forecast(bundle_in, db)
        forecast = Forecast(
            user_id=forecast_data.user_id,
            posting_id=post.posting_id,
            predicted_reservations=forecast_data.predicted_reservations,
            predicted_no_show_prob=forecast_data.predicted_no_show_prob
        )
        db.add(forecast)
    
    db.commit()

def seed_badges(db: Session):
    good_start = Badge(name="Good Start", detail="Make your first reservation")
    first_rescue = Badge(name="First Rescue", detail="Collect your first bundle")
    on_a_roll = Badge(name="On a Roll", detail="Collect a bundle for 3 days in a row")
    locked_in = Badge(name="Locked In", detail="Collect a bundle for 7 days in a row")
    relentless = Badge(name="Relentless", detail="Collect a bundle for 30 days in a row")
    waste_warrior = Badge(name="Waste Warrior", detail="Save 1kg of food")
    eco_advocate = Badge(name="Eco Advocate", detail="Save 10kg of food")
    green_guardian = Badge(name="Green Guardian", detail="Save 25kg of food")
    punctual = Badge(name="Punctual", detail="Complete 10 collections in a row with no no-shows")
    time_keeper = Badge(name="TimeKeeper", detail="Complete 25 collections in a row with no no-shows")
    unshakeable = Badge(name="Unshakeable", detail="Complete 50 collections in a row with no no-shows")
    final_call = Badge(name="Final Call", detail="Collect a bundle within the last 5 minutes of a pickup window")
    weatherproof = Badge(name="Weatherproof", detail="Collect 5 bundles in rainy weather")
    triple_threat = Badge(name="Triple Threat", detail="Collect 3 bundles in 1 day")
    familiar_face = Badge(name="Familiar Face", detail="Collect 3 bundles from the same seller")
    well_rounded = Badge(name="Well Rounded", detail="Collect a bundle from every food category")

    badges = [
        good_start, first_rescue, on_a_roll, locked_in, relentless,
        waste_warrior, eco_advocate, green_guardian, punctual, time_keeper,
        unshakeable, final_call, weatherproof, triple_threat, familiar_face,
        well_rounded
    ]
    for badge in badges:
        db.add(badge)

    db.commit()

def seed_issue_reports(db: Session):
    reservations = db.exec(select(Reservation)).all()

    reports_to_seed = 150
    
    for _ in range(reports_to_seed):
        reservation = fake.random_element(elements=reservations)
        
        status = fake.random_element(elements=list(ReportStatus))
        
        description, response = get_report_desc_and_response(status)
        
        issue_report = IssueReport(
            posting_id=reservation.posting_id,
            user_id=reservation.user_id,
            description=description,
            status=status,
            seller_response=response,
        )
        db.add(issue_report)
    
    db.commit()


def get_report_desc_and_response(status: ReportStatus):
    descriptions = [
        "Category on the post does not match items recieved.",
        "Incorrect allergens listed.",
        "Store closed when collecting.",
        "Items were past their expiration date.",
        "The bundle contained less food than advertised.",
        "The seller was rude during the collection process.",
        "The food quality was poor or unsafe to consume.",
        "The pickup location was difficult to find or inaccessible.",
        "The seller refused to provide the bundle despite a valid reservation.",
        "The packaging was damaged, causing the food to be contaminated.",
    ]

    seller_response =[
        "We apologize for the confusion. We will ensure our staff categorizes items correctly in the future.",
        "Thank you for bringing this to our attention. We have updated our allergen protocols immediately.",
        "We are very sorry for the inconvenience. Please contact support for a full refund.",
        "We strive for freshness and will investigate why these items were not removed from stock sooner.",
        "We apologize that the bundle did not meet expectations. We will review our portioning standards.",
        "We are sorry to hear about your experience. We are addressing this with our team internally.",
        "Safety is our priority. We have discarded the remaining batch and are investigating the cause.",
        "Thank you for the feedback. We will provide clearer instructions for finding our pickup point.",
        "We apologize for the error in our system. We are working to ensure this doesn't happen again.",
        "We are sorry for the damage. We will look into more robust packaging for our rescue bundles.",
    ]

    description = fake.random_element(elements=descriptions)
    index = descriptions.index(description)
    
    response = seller_response[index] if status in [ReportStatus.RESOLVED, ReportStatus.SELLER_RESPONDED] else None
    
    return description, response


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
        seed_badges(db=db)
        seed_issue_reports(db=db)
    print("Seeding complete")

if __name__ == "__main__":
    seed_tables()