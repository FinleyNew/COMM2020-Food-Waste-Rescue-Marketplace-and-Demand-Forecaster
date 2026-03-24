from sqlalchemy import Float, func, case, cast
from sqlmodel import Session
from app.models.record import Record
from app.models.bundlePosting import BundlePosting

_BAND_ORDER = {"0-10": 0, "11-20": 1, "21-30": 2, "31-40": 3, "41+": 4}


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