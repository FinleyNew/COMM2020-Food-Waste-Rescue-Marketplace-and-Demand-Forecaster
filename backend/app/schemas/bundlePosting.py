from sqlmodel import SQLModel

class BundlePostingBase(SQLModel):
    user_id: int
    category: str
    allergens: str
    available: int
    price: ?
    pickup_window: ?

class BundlePostingCreate(BundlePostingBase):
    pass

class BundlePostingPublic(BundlePostingBase):
    posting_id: int
    reserved: int
    status: ?