from enum import Enum

# These are enums that are used within models and schemas
# The enum to define what permissions a user has
class Role(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    CONSUMER = "consumer"

# The enum for the status of a reservation
class ReservationStatus(str, Enum):
    RESERVED = "reserved"
    COLLECTED = "collected"
    NO_SHOW = "no_show"

# The enum for the status of a bundle posting
class BundleStatus(str, Enum):
    AVAILABLE = "available"
    SOLD_OUT = "sold_out"
    EXPIRED = "expired"
    DELETED = "deleted"

# The enum for the status of a report
class ReportStatus(str, Enum):
    AWAITING_RESPONSE = "awaiting response"
    SELLER_RESPONDED = "seller responded"
    RESOLVED = "resolved"
