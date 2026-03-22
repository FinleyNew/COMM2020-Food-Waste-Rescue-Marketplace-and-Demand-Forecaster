import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.services.seller import create_seller
from sqlalchemy.exc import IntegrityError

# 1. TEST: EMAIL UNIQUENESS (A-R02)
# Your code already has: if user_crud.get_user_by_email(...): raise HTTPException
def test_prevent_duplicate_emails(mock_db):
    with patch("app.crud.user.get_user_by_email") as mock_get:
        mock_get.return_value = MagicMock(id=1) # Pretend email is taken
        
        user_in = MagicMock(email="test@exeter.ac.uk")
        with pytest.raises(HTTPException) as exc:
            create_seller(seller_in=MagicMock(), user_in=user_in, db=mock_db)
        
        assert exc.value.status_code == 400
        assert "already registered" in exc.value.detail

# 2. TEST: THE INVISIBLE HANDSHAKE (User ID Linkage)
# Your code has: user_id = user.user_id ... seller = seller_crud.create_seller(..., user_id=user_id)
def test_seller_registration_links_to_correct_user(mock_db):
    # Add a patch for 'get_user_by_email' to return None (meaning email is free)
    with patch("app.crud.user.get_user_by_email", return_value=None), \
         patch("app.crud.user.create_user") as mock_user_create, \
         patch("app.crud.seller.create_seller") as mock_seller_create, \
         patch("app.services.seller.get_coordinates", return_value=(50.7, -3.5)):

        # Simulate User creation returning ID 999
        mock_user_create.return_value = MagicMock(user_id=999)

        # Act
        # We use a real-ish email so the Mock doesn't get confused
        user_in = MagicMock(email="new_shop@exeter.ac.uk", password="123")
        create_seller(seller_in=MagicMock(), user_in=user_in, db=mock_db)

        # Assert: Did the seller get the ID 999?
        # Note: Your service uses 'user_id' as a keyword argument
        _, kwargs = mock_seller_create.call_args
        assert kwargs['user_id'] == 999

def test_registration_rollback_on_failure(mock_db):
    with patch("app.crud.user.get_user_by_email", return_value=None), \
         patch("app.crud.user.create_user", return_value=MagicMock(user_id=123)), \
         patch("app.services.seller.get_coordinates", return_value=(50.7, -3.5)), \
         patch("app.crud.seller.create_seller", side_effect=Exception("Database Crash!")):

        # 1. Provide a real-ish user_in with a string password
        user_in = MagicMock()
        user_in.email = "test@exeter.ac.uk"
        user_in.password = "Exeter123"  # <--- This fixes the TypeError

        # 2. Act
        with pytest.raises(Exception) as exc:
            create_seller(seller_in=MagicMock(), user_in=user_in, db=mock_db)

        # 3. Assert: Now it should actually reach the "Database Crash!"
        assert "Database Crash!" in str(exc.value)
        
        # 4. The Real Goal: Did the brain call rollback?
        # Note: If your code still says 'db.rollback' instead of 'db.rollback()', 
        # this line will fail, which proves the bug exists!
        mock_db.rollback.assert_called_once()

       

def test_registration_race_condition_protection(mock_db):
    """
    Test A-R02.1: Proves that even if the 'Email Exists' check is bypassed,
    the Database Unique Constraint (IntegrityError) prevents duplicates.
    """
    with patch("app.crud.user.get_user_by_email", return_value=None), \
         patch("app.crud.user.create_user") as mock_create:
        
        # 1. Simulate the "Race": The check passed (None), 
        # but when we actually try to save, Postgres says "Wait, someone just took this!"
        mock_create.side_effect = IntegrityError("duplicate key", params={}, orig=None)

        user_in = MagicMock(email="race@exeter.ac.uk", password="123")

        # 2. Act & Assert
        # Your service should catch this or allow the IntegrityError to bubble up
        with pytest.raises(IntegrityError):
            create_seller(seller_in=MagicMock(), user_in=user_in, db=mock_db)
            
        # THE INVISIBLE CHECK: Even in a race condition, did it try to rollback?
        mock_db.rollback.assert_called_once()