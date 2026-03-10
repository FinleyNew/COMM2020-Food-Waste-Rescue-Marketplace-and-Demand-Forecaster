from sqlmodel import Field, SQLModel

# The base schema for consumers
class ConsumerBase(SQLModel):
    # Ensures the name cannot be 0 chars long or more than 50
    display_name: str = Field(min_length=1, max_length=50)

# The create schema for consumers
# Currently not in use
class ConsumerCreate(ConsumerBase):
    pass

#The public schema for consumers
class ConsumerPublic(ConsumerBase):
    user_id: int
    # Streak cannot be negative
    streak: int = Field(ge=0)