from sqlmodel import SQLModel

class BundleBase(SQLModel):
    user_id: int
    category: str
    allergens: str
    available: int
    price: str
    pickup_window: int

class BundleCreate(BundleBase):
    pass

class BundlePublic(BundleBase):
    posting_id: int
    reserved: int
    status: ?