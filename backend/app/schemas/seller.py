from sqlmodel import SQLModel

class SellerBase(SQLModel):
    name: str
    location: str
    open_hours: str

class SellerPublic(SellerBase):
    user_id: int