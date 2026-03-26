from pydantic import BaseModel
from typing import List

# The schema for outcome breakdowns
# Used in sell breakdown
class OutcomeBreakdownItem(BaseModel):
    label: str
    value: int
    pct: float

# The schema for a sellers sell breakdown
class SellerSellThroughBreakdown(BaseModel):
    total_posted: int
    total_collected: int
    total_no_shows: int
    total_expired: int
    collected_pct_of_posted: float
    no_show_pct_of_posted: float
    expired_pct_of_posted: float
    outcome_breakdown: List[OutcomeBreakdownItem]

# The schema for discount band metrics
class DiscountBandMetrics(BaseModel):
    discount_band: str
    posted_units: int
    reserved_units: int
    collected_units: int
    no_show_units: int
    expired_units: int
    sell_through_rate: float
    reservation_conversion_rate: float
    no_show_rate: float

# The schema for pickup window operational metrics
class PickupWindowOperationalMetrics(BaseModel):
    pickup_window: str
    posted_units: int
    reserved_units: int
    collected_units: int
    no_show_units: int
    expired_units: int
    sell_through_rate: float
    no_show_rate: float

# The schema for category operational metrics
class CategoryOperationalMetrics(BaseModel):
    category: str
    posted_units: int
    reserved_units: int
    collected_units: int
    sell_through_rate: float

# The schema for best pickup window by sell through rate
class BestPickupWindowBySellThrough(BaseModel):
    pickup_window: str
    sell_through_rate: float

# The schema for worst pickup window by no show
class WorstPickupWindowByNoShow(BaseModel):
    pickup_window: str
    no_show_rate: float

# The schema for most popular category by reservations
class MostPopularCategoryByReservations(BaseModel):
    category: str
    reserved_units: int

# The schema for seller operational insights
class SellerOperationalInsights(BaseModel):
    pickup_windows: List[PickupWindowOperationalMetrics]
    categories: List[CategoryOperationalMetrics]
    best_pickup_window_by_sell_through: BestPickupWindowBySellThrough | None
    worst_pickup_window_by_no_show: WorstPickupWindowByNoShow | None
    most_popular_category_by_reservations: MostPopularCategoryByReservations | None

# The schema for Sellers analytics summary
class SellerAnalyticsSummary(BaseModel):
    total_bundle_postings: int
    total_posted: int
    total_reserved: int
    total_collected: int
    total_no_shows: int
    total_expired: int
    reservation_conversion_rate: float
    sell_through_rate: float
    no_show_rate: float
    expiry_rate: float
    waste_avoided_kg: float

# The schema for a consumers personal impact summary
class ConsumerPersonalImpactSummary(BaseModel):
    total_reservations_made: int
    total_collected: int
    total_no_shows: int
    collection_success_rate: float
    waste_saved_kg: float
    co2_estimate_saved: float
    favourite_category: str | None
    collections_this_month: int
    streak: int
    badges_earned: int