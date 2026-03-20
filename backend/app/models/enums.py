from enum import Enum

# These are enums that are used within models and schemas
class Role(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    CONSUMER = "consumer"

class ReservationStatus(str, Enum):
    RESERVED = "reserved"
    COLLECTED = "collected"
    NO_SHOW = "no_show"

class BundleStatus(str, Enum):
    AVAILABLE = "available"
    SOLD_OUT = "sold_out"
    EXPIRED = "expired"
    DELETED = "deleted"

class Category(str, Enum):
    BAKED_GOODS = "Baked Goods"
    FRUIT = "Fruit"
    VEGETABLES = "Vegetables"
    MEAT = "Meat"
    SEAFOOD = "Seafood"
    SNACKS = "Snacks"
    DAIRY = "Dairy"
    DRINKS = "Drinks"

class ReportType(str, Enum):
    SELLER_ISSUE = "seller issue"
    DEVELOPER_ISSUE = "developer issue"

class ReportStatus(str, Enum):
    AWAITING_RESPONSE = "awaiting response"
    SELLER_RESPONDED = "seller responded"
    RESOLVED = "resolved"