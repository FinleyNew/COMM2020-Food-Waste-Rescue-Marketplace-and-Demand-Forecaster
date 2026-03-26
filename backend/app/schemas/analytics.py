from pydantic import BaseModel
from typing import List

# A single outcome row (collected / no_show / expired) with count and percentage
class OutcomeBreakdownItem(BaseModel):
    label: str
    value: int
    pct: float

# Sell-through breakdown showing how posted units ended up
class SellerSellThroughBreakdown(BaseModel):
    total_posted: int
    total_collected: int
    total_no_shows: int
    total_expired: int
    collected_pct_of_posted: float
    no_show_pct_of_posted: float
    expired_pct_of_posted: float
    outcome_breakdown: List[OutcomeBreakdownItem]

# Pricing metrics grouped by discount band (0-10%, 11-20%, 21-30%, 31-40%, 41%+)
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

# Performance metrics for a single pickup time slot
class PickupWindowOperationalMetrics(BaseModel):
    pickup_window: str  # e.g. "12:00 - 13:00"
    posted_units: int
    reserved_units: int
    collected_units: int
    no_show_units: int
    expired_units: int
    sell_through_rate: float
    no_show_rate: float

# Performance metrics for a single food category
class CategoryOperationalMetrics(BaseModel):
    category: str
    posted_units: int
    reserved_units: int
    collected_units: int
    sell_through_rate: float

# The pickup window with the highest sell-through rate
class BestPickupWindowBySellThrough(BaseModel):
    pickup_window: str
    sell_through_rate: float

# The pickup window with the highest no-show rate
class WorstPickupWindowByNoShow(BaseModel):
    pickup_window: str
    no_show_rate: float

# The food category with the most reservations
class MostPopularCategoryByReservations(BaseModel):
    category: str
    reserved_units: int

# Combined operational insights: per-window, per-category, and highlights
class SellerOperationalInsights(BaseModel):
    pickup_windows: List[PickupWindowOperationalMetrics]
    categories: List[CategoryOperationalMetrics]
    best_pickup_window_by_sell_through: BestPickupWindowBySellThrough | None
    worst_pickup_window_by_no_show: WorstPickupWindowByNoShow | None
    most_popular_category_by_reservations: MostPopularCategoryByReservations | None

# High-level aggregate counts and rates for a seller
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

# A consumer's lifetime activity, environmental impact, and gamification stats
class ConsumerPersonalImpactSummary(BaseModel):
    total_reservations_made: int
    total_collected: int
    total_no_shows: int
    collection_success_rate: float
    waste_saved_kg: float
    co2_estimate_saved: float  # uses 2.5 kg CO2 per kg food
    favourite_category: str | None
    collections_this_month: int
    streak: int
    badges_earned: int