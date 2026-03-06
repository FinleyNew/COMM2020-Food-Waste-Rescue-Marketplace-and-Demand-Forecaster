from pydantic import BaseModel

# The schema for sending tokens
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# The schema for recieving/validating tokens
class TokenPayload(BaseModel):
    sub: str | None = None