from sqlalchemy import func
from sqlmodel import Session
from app.models.record import Record


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