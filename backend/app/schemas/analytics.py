from pydantic import BaseModel
from typing import List


class OutcomeBreakdownItem(BaseModel):
    label: str
    value: int
    pct: float


class SellerSellThroughBreakdown(BaseModel):
    total_posted: int
    total_collected: int
    total_no_shows: int
    total_expired: int
    collected_pct_of_posted: float
    no_show_pct_of_posted: float
    expired_pct_of_posted: float
    outcome_breakdown: List[OutcomeBreakdownItem]


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


class PickupWindowOperationalMetrics(BaseModel):
    pickup_window: str
    posted_units: int
    reserved_units: int
    collected_units: int
    no_show_units: int
    expired_units: int
    sell_through_rate: float
    no_show_rate: float


class CategoryOperationalMetrics(BaseModel):
    category: str
    posted_units: int
    reserved_units: int
    collected_units: int
    sell_through_rate: float


class BestPickupWindowBySellThrough(BaseModel):
    pickup_window: str
    sell_through_rate: float


class WorstPickupWindowByNoShow(BaseModel):
    pickup_window: str
    no_show_rate: float


class MostPopularCategoryByReservations(BaseModel):
    category: str
    reserved_units: int


class SellerOperationalInsights(BaseModel):
    pickup_windows: List[PickupWindowOperationalMetrics]
    categories: List[CategoryOperationalMetrics]
    best_pickup_window_by_sell_through: BestPickupWindowBySellThrough | None
    worst_pickup_window_by_no_show: WorstPickupWindowByNoShow | None
    most_popular_category_by_reservations: MostPopularCategoryByReservations | None


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