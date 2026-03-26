from datetime import datetime, timedelta, timezone

import jwt
from app.core.config import settings

import bcrypt

# The algorithm used for access tokens
ALGORITHM = "HS256"

# This function verifies the plain text password against the hashed password to ensure they're the same
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# This function returns the hashed password of the plain text entered
def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# This function returns a JWT from the user ID and the expire time for that token
def create_access_token(subject: int, expires_delta: timedelta = timedelta(hours=8)):
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)