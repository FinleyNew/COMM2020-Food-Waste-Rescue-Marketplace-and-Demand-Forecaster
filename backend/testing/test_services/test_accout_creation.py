"""
Tests the seller and consumer registration services and the Pydantic
schema validators that protect data quality at sign-up time.

Covers:
  - Consumer registration (no location/geocoding required)
  - Seller registration (coordinate lookup via get_coordinates)
  - Duplicate-email rejection for both seller and consumer paths
  - Consumer display_name length constraints
  - Seller opening-hours format and logic validation
  - Input whitespace trimming on email and seller name
"""

import pytest
from datetime import time
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from pydantic import ValidationError
from app.services.seller import create_seller
from app.services.consumer import create_consumer
from sqlalchemy.exc import IntegrityError



@pytest.fixture
def mock_db():
   
    return MagicMock()



# These tests verify the create_seller and create_consumer service
# tests the different validation rules and logic in each path


def test_consumer_creation_does_not_need_location(mock_db):
    # Consumers should be able to register without providing a location.
    # Unlike sellers, the consumer path must NOT call get_coordinates.
    
    with patch("app.crud.user.get_user_by_email", return_value=None), \
         patch("app.crud.user.create_user", return_value=MagicMock(user_id=2)), \
         patch("app.crud.consumer.create_consumer", return_value=MagicMock()) as mock_create, \
         patch("app.services.seller.get_coordinates") as mock_geocode:

        user_in = MagicMock()
        user_in.email = "consumer@exeter.ac.uk"
        user_in.password = "Password123"

        from app.schemas.consumer import ConsumerCreate
        cons_in = ConsumerCreate(display_name="Student")

        create_consumer(consumer_in=cons_in, user_in=user_in, db=mock_db)
        mock_create.assert_called_once()
        mock_geocode.assert_not_called()

def test_seller_needs_location_and_coordinates(mock_db):
    # Sellers must provide a location that can be geocoded into coordinates.
    with patch("app.crud.user.get_user_by_email", return_value=None), \
         patch("app.crud.user.create_user", return_value=MagicMock(user_id=3)), \
         patch("app.crud.seller.create_seller", return_value=MagicMock()) as mock_create, \
         patch("app.services.seller.get_coordinates", return_value=(50.7, -3.5)) as mock_geocode:
        user_in = MagicMock()
        user_in.email = "shop@exeter.ac.uk"
        user_in.password = "Password123"
        seller_in = MagicMock()
        seller_in.name = "Test Shop"
        seller_in.location = "Exeter High Street"
        seller_in.opening_hours = "09:00 - 17:00"
        create_seller(seller_in=seller_in, user_in=user_in, db=mock_db)
        mock_geocode.assert_called_once_with("Exeter High Street")
        mock_create.assert_called_once()
        assert mock_create.call_args.kwargs['latitude'] == 50.7
        assert mock_create.call_args.kwargs['longitude'] == -3.5


# The system must prevent two accounts sharing the same email address.
# The service checks first (get_user_by_email), and the database has a
# unique constraint as a second safety net.

def test_prevent_duplicate_emails(mock_db):
   # When get_user_by_email finds an existing user, the service must raise an HTTPException and not call create_user.
    with patch("app.crud.user.get_user_by_email") as mock_get:
        mock_get.return_value = MagicMock(id=1)

        user_in = MagicMock(email="test@exeter.ac.uk")
        with pytest.raises(HTTPException) as exc:
            create_seller(seller_in=MagicMock(), user_in=user_in, db=mock_db)

        assert exc.value.status_code == 400
        assert "already registered" in exc.value.detail


def test_consumer_duplicate_email_rejected(mock_db):
    # Similar to the seller test, but for consumer creation.
    with patch("app.crud.user.get_user_by_email", return_value=MagicMock(id=1)):
        user_in = MagicMock(email="taken@exeter.ac.uk")
        from app.schemas.consumer import ConsumerCreate
        with pytest.raises(HTTPException) as exc:
            create_consumer(consumer_in=ConsumerCreate(display_name="Student"), user_in=user_in, db=mock_db)
        assert exc.value.status_code == 400
        assert "already registered" in exc.value.detail




def test_consumer_empty_display_name_rejected():
    # An empty string for display_name must be rejected by the schema.
    
    from app.schemas.consumer import ConsumerCreate
    with pytest.raises(ValidationError) as exc:
        ConsumerCreate(display_name="")
    assert "display_name" in str(exc.value).lower()


def test_consumer_display_name_too_long_rejected():
    # A display_name longer than 50 characters must be rejected by the schema.
    from app.schemas.consumer import ConsumerCreate
    with pytest.raises(ValidationError) as exc:
        ConsumerCreate(display_name="A" * 51)
    assert "display_name" in str(exc.value).lower()




def test_seller_opening_after_closing_rejected():
    # If the opening_hours string has a closing time that is earlier than the opening time, it must be rejected by the schema.
    from app.schemas.seller import SellerCreate

    with pytest.raises(ValidationError) as exc:
        SellerCreate(
            name="Test Shop",
            location="Exeter High Street",
            opening_hours="18:00 - 09:00",
            logo_url="https://example.com/logo.png",
        )
    assert "closing time must be after opening time" in str(exc.value).lower()


def test_seller_valid_hours_accepted():
    # A valid opening_hours string (e.g. "09:00 - 17:00") should be accepted 
    from app.schemas.seller import SellerCreate

    seller = SellerCreate(
        name="Test Shop",
        location="Exeter High Street",
        opening_hours="09:00 - 17:00",
        logo_url="https://example.com/logo.png",
    )
    assert seller.opening_hours == "09:00 - 17:00"


def test_seller_invalid_hours_format_rejected():
    # If the opening_hours string is not in the correct format (e.g. "9 to 5"), it must be rejected by the schema.
    from app.schemas.seller import SellerCreate

    with pytest.raises(ValidationError):
        SellerCreate(
            name="Test Shop",
            location="Exeter High Street",
            opening_hours="nine to five",
            logo_url="https://example.com/logo.png",
        )



def test_email_whitespace_trimmed_on_user_create():
    # Leading/trailing spaces on the email should be stripped during user creation to prevent duplicate accounts and login issues.
    from app.schemas.user import UserCreate
    user = UserCreate(
        email="  user@exeter.ac.uk  ",
        password="Password123",
    )
    assert user.email == "user@exeter.ac.uk"


def test_seller_name_whitespace_trimmed():
    # Leading/trailing spaces on the seller name should be stripped by the schema validator to ensure consistent display and prevent duplicates.
    from app.schemas.seller import SellerCreate
    seller = SellerCreate(
        name="  Exeter Cafe  ",
        location="High Street",
        opening_hours="09:00 - 17:00",
        logo_url="https://example.com/logo.png",
    )
    assert seller.name == "Exeter Cafe"






