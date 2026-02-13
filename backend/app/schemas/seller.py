from sqlmodel import SQLModel

# The base schema for sellers
class SellerBase(SQLModel):
    name: str
    location: str
    open_hours: str

#No create schema as we cannot create users yet

# The public schema for seller
class SellerPublic(SellerBase):
    user_id: int