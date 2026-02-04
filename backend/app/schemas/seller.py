from sqlmodel import SQLModel

class SellerBase(SQLModel):
    name: str
    location: ?
    open_hours: ?

class SellerPublic(SellerBase):
    id: int