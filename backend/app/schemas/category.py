from sqlmodel import SQLModel

# The base schema for category
class CategoryBase(SQLModel):
    name: str

# The create schema for category
class CategoryCreate(CategoryBase):
    pass

# The public schema for category
class CategoryPublic(CategoryBase):
    category_id: int