from sqlmodel import SQLModel

class ConsumerBase(SQLModel):
    display_name: str

class ConsumerCreate(ConsumerBase):
    #password: str
    pass

class ConsumerPublic(ConsumerBase):
    user_id: int
    streak: int