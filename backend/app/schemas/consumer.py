from sqlmodel import SQLModel

class ConsumerBase(SQLModel):
    display_name: str

class ConsumerCreate(ConsumerBase):
    password: str

class ConsumerPublic(ConsumerBase):
    id: int
    streak: int