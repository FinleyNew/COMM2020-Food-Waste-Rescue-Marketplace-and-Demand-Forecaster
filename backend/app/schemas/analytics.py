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