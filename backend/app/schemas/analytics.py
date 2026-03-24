from pydantic import BaseModel

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