from sqlmodel import SQLModel

# The base schema for consumers
class ConsumerBase(SQLModel):
    display_name: str

# The create schema for consumers
# Currently not in use
class ConsumerCreate(ConsumerBase):
    #password: str
    pass

#The public schema for consumers
class ConsumerPublic(ConsumerBase):
    user_id: int
    streak: int