"""
Tests the core security functions that protect user accounts:
password hashing (bcrypt), JWT token generation, SQL-injection
resistance, and password change hashing.

"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from jwt import decode as jwt_decode

from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.services import user as user_service
from sqlmodel.sql.expression import Select, SelectOfScalar

ALGORITHM = "HS256"




@pytest.fixture
def mock_db():
    
    return MagicMock()


@pytest.fixture
def mock_user():
    
    user = MagicMock()
    user.user_id = 1
    user.email = "test@exeter.ac.uk"
    user.hashed_password = get_password_hash("Password123")
    user.is_locked = False
    user.failed_login_count = 0
    return user


# Passwords must never be stored in plain text. The application uses bcrypt which produces a salted one-way hash. These tests verify:
#   - The hash differs from the original password
#   - The hash is in bcrypt format ($2b$ prefix)
#   - Correct passwords verify successfully
#   - Wrong passwords are rejected
#   - Each hash is unique due to random salt

def test_hash_password_is_not_plaintext():
    # Hashing a password should produce a different string than the original. Or else its pretty useless
    plain = "Password123"
    hashed = get_password_hash(plain)
    assert hashed != plain


def test_hash_password_is_bcrypt_format():
    # The hash should start with $2b$ which indicates bcrypt format.
    hashed = get_password_hash("Password123")
    assert hashed.startswith("$2b$"), f"Expected bcrypt hash, got: {hashed[:10]}..."


def test_verify_password_correct():
    # verify_password should return True for the correct password.
    plain = "Password123"
    hashed = get_password_hash(plain)
    assert verify_password(plain, hashed) is True


def test_verify_password_wrong():
    # verify_password should return False for an incorrect password.
    hashed = get_password_hash("Password123")
    assert verify_password("WrongPassword", hashed) is False


def test_same_password_hashes_differently():
    # Hashing the same password twice should produce different hashes due to random salting.
    h1 = get_password_hash("Password123")
    h2 = get_password_hash("Password123")
    assert h1 != h2, "Two hashes of the same password should differ due to salting"


# After successful login the server issues a JSON Web Token (JWT).
# These tests decode the token with the real secret key and verify
# the claims are present, correct, and time-bounded.

def test_jwt_token_contains_exp_claim():
    # Every JWT must contain an 'exp' (expiry) claim that is a timestamp in the future.
    token = create_access_token(subject=1)
    payload = jwt_decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload


def test_jwt_token_contains_sub_claim(mock_user):
    # Every JWT must contain a 'sub' (subject) claim that matches the user_id of the authenticated user.
    token = create_access_token(subject=mock_user.user_id)
    assert token is not None
    assert isinstance(token, str)
    payload = jwt_decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload
    assert "sub" in payload


def test_jwt_token_expires_in_expected_window():
    # The 'exp' claim must be a timestamp that is reasonably far in the future (e.g. 8 hours) but not unreasonably far (e.g. 10 years).
    before = datetime.now(timezone.utc)
    token = create_access_token(subject=1)
    after = datetime.now(timezone.utc)
    payload = jwt_decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    assert exp > after, "Token expiry must be in the future"
    max_expiry = after + timedelta(days=7)
    assert exp <= max_expiry, f"Token expiry {exp} is unreasonably far in the future"
    token_lifetime = exp - before
    assert token_lifetime.total_seconds() > 60, "Token lifetime must be more than 1 minute"


def test_jwt_token_subject_matches():
    # The 'sub' claim must match the subject (user_id) provided when creating the token.
    token = create_access_token(subject=42)
    payload = jwt_decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    assert str(payload["sub"]) == "42"



# SQLModel/SQLAlchemy uses parameterised queries by default, but this test verifies the CRUD layer is actually using a Select object rather than building a raw SQL string.

def test_query_uses_parameterized_statements(mock_db):
    # When get_user_by_email is called, it should construct a Select or SelectOfScalar object rather than a raw SQL string. This ensures SQL-injection resistance.
    from app.crud.user import get_user_by_email
    get_user_by_email(email="test@exeter.ac.uk", db=mock_db)
    args, _ = mock_db.exec.call_args
    assert isinstance(args[0], (Select, SelectOfScalar))



# When a user changes their password through the update_user service, the new password must be hashed before it reaches the CRUD layer.

def test_update_user_hashes_password(mock_db):
   # When the user updates their password, the service should hash it before passing to CRUD.
    from app.schemas.user import UserUpdate
    mock_user = MagicMock()
    update = UserUpdate(password="NewPassword123")
    with patch("app.crud.user.update_user", return_value=mock_user):
        user_service.update_user(current_user=mock_user, user_update=update, db=mock_db)
        assert update.password != "NewPassword123"
        assert update.password.startswith("$2b$")


def test_update_user_no_password_no_hash(mock_db):
    # If the update does not include a password, the service should not add one or try to hash it.
    from app.schemas.user import UserUpdate
    mock_user = MagicMock()
    update = UserUpdate(email="new@exeter.ac.uk")
    with patch("app.crud.user.update_user", return_value=mock_user) as mock_crud:
        user_service.update_user(current_user=mock_user, user_update=update, db=mock_db)
        assert update.password is None
        mock_crud.assert_called_once()
