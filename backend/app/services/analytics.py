from datetime import datetime, timezone

from sqlalchemy import Float, Time, func, case, cast
from sqlmodel import Session
from app.models.record import Record
from app.models.bundlePosting import BundlePosting, Category
from app.models.consumer import Consumer
from app.models.badge import ConsumerBadge
from app.models.reservation import Reservation
from app.models.enums import ReservationStatus

_BAND_ORDER = {"0-10": 0, "11-20": 1, "21-30": 2, "31-40": 3, "41+": 4}
_CO2_KG_PER_KG_FOOD = 2.5


def get_consumer_personal_impact_summary(consumer_id: int, db: Session) -> dict:
    now_utc = datetime.now(timezone.utc)
    month_start_utc = now_utc.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    reservation_stats = (
        db.query(
            func.count(Reservation.reservation_id).label("total_reservations_made"),
            func.sum(
                case((Reservation.status == ReservationStatus.COLLECTED, 1), else_=0)
            ).label("total_collected"),
            func.sum(
                case((Reservation.status == ReservationStatus.NO_SHOW, 1), else_=0)
            ).label("total_no_shows"),
            func.sum(
                case(
                    (Reservation.status == ReservationStatus.COLLECTED, BundlePosting.weight),
                    else_=0,
                )
            ).label("waste_saved_grams"),
        )
        .outerjoin(BundlePosting, BundlePosting.posting_id == Reservation.posting_id)
        .filter(Reservation.user_id == consumer_id)
        .first()
    )

    favourite_category = (
        db.query(Category.name)
        .join(BundlePosting, BundlePosting.category_id == Category.category_id)
        .join(Reservation, Reservation.posting_id == BundlePosting.posting_id)
        .filter(Reservation.user_id == consumer_id)
        .filter(Reservation.status == ReservationStatus.COLLECTED)
        .group_by(Category.name)
        .order_by(func.count(Reservation.reservation_id).desc(), Category.name.asc())
        .first()
    )

    collections_this_month = (
        db.query(func.count(Reservation.reservation_id))
        .filter(Reservation.user_id == consumer_id)
        .filter(Reservation.status == ReservationStatus.COLLECTED)
        .filter(Reservation.timestamp >= month_start_utc)
        .scalar()
    ) or 0

    consumer_streak = (
        db.query(Consumer.streak)
        .filter(Consumer.user_id == consumer_id)
        .scalar()
    ) or 0

    badges_earned = (
        db.query(func.count(ConsumerBadge.badge_id))
        .filter(ConsumerBadge.user_id == consumer_id)
        .scalar()
    ) or 0

    total_reservations_made = reservation_stats.total_reservations_made or 0
    total_collected = reservation_stats.total_collected or 0
    total_no_shows = reservation_stats.total_no_shows or 0
    waste_saved_grams = reservation_stats.waste_saved_grams or 0
    waste_saved_kg = float(waste_saved_grams) / 1000.0

    collection_success_rate = 0.0
    if total_reservations_made > 0:
        collection_success_rate = (total_collected / total_reservations_made) * 100

    return {
        "total_reservations_made": total_reservations_made,
        "total_collected": total_collected,
        "total_no_shows": total_no_shows,
        "collection_success_rate": round(collection_success_rate, 2),
        "waste_saved_kg": round(waste_saved_kg, 2),
        "co2_estimate_saved": round(waste_saved_kg * _CO2_KG_PER_KG_FOOD, 2),
        "favourite_category": favourite_category[0] if favourite_category else None,
        "collections_this_month": collections_this_month,
        "streak": consumer_streak,
        "badges_earned": badges_earned,
    }


def get_seller_operational_insights(seller_id: int, db: Session) -> dict:
    pickup_start_expr = cast(func.lower(Record.pickup_window), Time)
    pickup_end_expr = cast(func.upper(Record.pickup_window), Time)

    pickup_rows = (
        db.query(
            pickup_start_expr.label("pickup_start"),
            pickup_end_expr.label("pickup_end"),
            func.sum(Record.observed_reservations).label("reserved_units"),
            func.sum(Record.observed_no_show).label("no_show_units"),
            func.sum(Record.observed_expired).label("expired_units"),
        )
        .filter(Record.user_id == seller_id)
        .group_by(pickup_start_expr, pickup_end_expr)
        .all()
    )

    pickup_windows = []
    for row in pickup_rows:
        reserved = row.reserved_units or 0
        no_shows = row.no_show_units or 0
        expired = row.expired_units or 0
        collected = max(reserved - no_shows, 0)
        posted = reserved + expired
        pickup_window_label = f"{row.pickup_start.strftime('%H:%M')} - {row.pickup_end.strftime('%H:%M')}"

        pickup_windows.append({
            "pickup_window": pickup_window_label,
            "posted_units": posted,
            "reserved_units": reserved,
            "collected_units": collected,
            "no_show_units": no_shows,
            "expired_units": expired,
            "sell_through_rate": round((collected / posted) * 100, 2) if posted > 0 else 0.0,
            "no_show_rate": round((no_shows / reserved) * 100, 2) if reserved > 0 else 0.0,
        })

    pickup_windows.sort(key=lambda item: item["pickup_window"])

    category_rows = (
        db.query(
            Category.name.label("category"),
            func.sum(Record.observed_reservations).label("reserved_units"),
            func.sum(Record.observed_no_show).label("no_show_units"),
            func.sum(Record.observed_expired).label("expired_units"),
        )
        .join(Category, Category.category_id == Record.category_id)
        .filter(Record.user_id == seller_id)
        .group_by(Category.name)
        .all()
    )

    categories = []
    for row in category_rows:
        reserved = row.reserved_units or 0
        no_shows = row.no_show_units or 0
        expired = row.expired_units or 0
        collected = max(reserved - no_shows, 0)
        posted = reserved + expired

        categories.append({
            "category": row.category,
            "posted_units": posted,
            "reserved_units": reserved,
            "collected_units": collected,
            "sell_through_rate": round((collected / posted) * 100, 2) if posted > 0 else 0.0,
        })

    categories.sort(key=lambda item: item["category"])

    best_pickup_window_by_sell_through = None
    if pickup_windows:
        best_pickup_window = max(
            pickup_windows,
            key=lambda item: item["sell_through_rate"],
        )
        best_pickup_window_by_sell_through = {
            "pickup_window": best_pickup_window["pickup_window"],
            "sell_through_rate": best_pickup_window["sell_through_rate"],
        }

    worst_pickup_window_by_no_show = None
    if pickup_windows:
        worst_pickup_window = max(
            pickup_windows,
            key=lambda item: item["no_show_rate"],
        )
        worst_pickup_window_by_no_show = {
            "pickup_window": worst_pickup_window["pickup_window"],
            "no_show_rate": worst_pickup_window["no_show_rate"],
        }

    most_popular_category_by_reservations = None
    if categories:
        most_popular_category = max(
            categories,
            key=lambda item: item["reserved_units"],
        )
        most_popular_category_by_reservations = {
            "category": most_popular_category["category"],
            "reserved_units": most_popular_category["reserved_units"],
        }

    return {
        "pickup_windows": pickup_windows,
        "categories": categories,
        "best_pickup_window_by_sell_through": best_pickup_window_by_sell_through,
        "worst_pickup_window_by_no_show": worst_pickup_window_by_no_show,
        "most_popular_category_by_reservations": most_popular_category_by_reservations,
    }


def get_seller_pricing_effectiveness(seller_id: int, db: Session) -> list:
    # Discount % = (initial_price - price) / initial_price * 100
    # initial_price lives on BundlePosting, so we join on posting_id.
    discount_pct_expr = case(
        (
            BundlePosting.initial_price > 0,
            (cast(BundlePosting.initial_price, Float) - cast(Record.price, Float))
            / cast(BundlePosting.initial_price, Float)
            * 100,
        ),
        else_=0.0,
    )

    band_expr = case(
        (discount_pct_expr <= 10, "0-10"),
        (discount_pct_expr <= 20, "11-20"),
        (discount_pct_expr <= 30, "21-30"),
        (discount_pct_expr <= 40, "31-40"),
        else_="41+",
    )

    rows = (
        db.query(
            band_expr.label("discount_band"),
            func.sum(Record.observed_reservations).label("reserved_units"),
            func.sum(Record.observed_no_show).label("no_show_units"),
            func.sum(Record.observed_expired).label("expired_units"),
        )
        .join(BundlePosting, Record.posting_id == BundlePosting.posting_id)
        .filter(Record.user_id == seller_id)
        .group_by(band_expr)
        .all()
    )

    bands = []
    for row in sorted(rows, key=lambda r: _BAND_ORDER.get(r.discount_band, 99)):
        reserved = row.reserved_units or 0
        no_shows = row.no_show_units or 0
        expired = row.expired_units or 0
        collected = max(reserved - no_shows, 0)
        posted = reserved + expired

        bands.append({
            "discount_band": row.discount_band,
            "posted_units": posted,
            "reserved_units": reserved,
            "collected_units": collected,
            "no_show_units": no_shows,
            "expired_units": expired,
            "sell_through_rate": round((collected / posted) * 100, 2) if posted > 0 else 0.0,
            "reservation_conversion_rate": round((collected / reserved) * 100, 2) if reserved > 0 else 0.0,
            "no_show_rate": round((no_shows / reserved) * 100, 2) if reserved > 0 else 0.0,
        })

    return bands


def get_seller_sell_through_breakdown(seller_id: int, db: Session) -> dict:
    result = db.query(
        func.sum(Record.observed_reservations).label("total_reserved"),
        func.sum(Record.observed_no_show).label("total_no_shows"),
        func.sum(Record.observed_expired).label("total_expired"),
    ).filter(Record.user_id == seller_id).first()

    total_reserved = result.total_reserved or 0
    total_no_shows = result.total_no_shows or 0
    total_expired = result.total_expired or 0
    total_collected = max(total_reserved - total_no_shows, 0)
    total_posted = total_reserved + total_expired

    collected_pct_of_posted = 0.0
    no_show_pct_of_posted = 0.0
    expired_pct_of_posted = 0.0
    if total_posted > 0:
        collected_pct_of_posted = (total_collected / total_posted) * 100
        no_show_pct_of_posted = (total_no_shows / total_posted) * 100
        expired_pct_of_posted = (total_expired / total_posted) * 100

    return {
        "total_posted": total_posted,
        "total_collected": total_collected,
        "total_no_shows": total_no_shows,
        "total_expired": total_expired,
        "collected_pct_of_posted": round(collected_pct_of_posted, 2),
        "no_show_pct_of_posted": round(no_show_pct_of_posted, 2),
        "expired_pct_of_posted": round(expired_pct_of_posted, 2),
        "outcome_breakdown": [
            {"label": "collected", "value": total_collected, "pct": round(collected_pct_of_posted, 2)},
            {"label": "no_show", "value": total_no_shows, "pct": round(no_show_pct_of_posted, 2)},
            {"label": "expired", "value": total_expired, "pct": round(expired_pct_of_posted, 2)},
        ],
    }


def get_seller_analytics_summary(seller_id: int, db: Session) -> dict:
    # Aggregate data from Record table for the seller.
    # Note: total_posted is interpreted as total bundle units posted,
    # not number of posting records.
    result = db.query(
        func.count(Record.record_id).label("total_bundle_postings"),
        func.sum(Record.observed_reservations).label("total_reserved"),
        func.sum(Record.observed_no_show).label("total_no_shows"),
        func.sum(Record.observed_expired).label("total_expired"),
        func.sum(Record.weight * (Record.observed_reservations - Record.observed_no_show)).label("waste_avoided_grams")
    ).filter(Record.user_id == seller_id).first()

    total_bundle_postings = result.total_bundle_postings or 0
    total_reserved = result.total_reserved or 0
    total_no_shows = result.total_no_shows or 0
    total_expired = result.total_expired or 0
    total_collected = max(total_reserved - total_no_shows, 0)
    waste_avoided_grams = result.waste_avoided_grams or 0.0
    waste_avoided_kg = float(waste_avoided_grams) / 1000.0

    # Unit-based denominator: offered units = reserved units + units that expired unsold
    total_units_posted = total_reserved + total_expired
    total_posted = total_units_posted

    # Calculate rates
    reservation_conversion_rate = 0.0
    if total_reserved > 0:
        reservation_conversion_rate = (total_collected / total_reserved) * 100

    sell_through_rate = 0.0
    if total_posted > 0:
        sell_through_rate = (total_collected / total_posted) * 100

    no_show_rate = 0.0
    if total_reserved > 0:
        no_show_rate = (total_no_shows / total_reserved) * 100

    expiry_rate = 0.0
    if total_units_posted > 0:
        expiry_rate = (total_expired / total_units_posted) * 100

    return {
        "total_bundle_postings": total_bundle_postings,
        "total_posted": total_posted,
        "total_reserved": total_reserved,
        "total_collected": total_collected,
        "total_no_shows": total_no_shows,
        "total_expired": total_expired,
        "reservation_conversion_rate": round(reservation_conversion_rate, 2),
        "sell_through_rate": round(sell_through_rate, 2),
        "no_show_rate": round(no_show_rate, 2),
        "expiry_rate": round(expiry_rate, 2),
        "waste_avoided_kg": round(waste_avoided_kg, 2)
    }