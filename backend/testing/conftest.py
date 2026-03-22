import pytest
from unittest.mock import MagicMock
import sys
import os
from datetime import datetime, timedelta

# Adds the 'backend' directory to the path automatically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_db():
    """Centralized Mock Database Session with standard SQLAlchemy behaviors."""
    db = MagicMock()
    db.commit.return_value = None
    db.add.return_value = None
    db.refresh.return_value = None
    return db

# --- General Class Factories ---

@pytest.fixture
def mock_user():
    """Generic User Mock: Customize streak and dates inside your tests."""
    user = MagicMock()
    user.id = 1
    user.email = "test@exeter.ac.uk"
    user.role = "consumer"
    user.streak = 0
    user.last_reservation_date = datetime.now()
    return user

@pytest.fixture
def mock_bundle():
    """Generic Bundle Mock: Customize availability and price."""
    bundle = MagicMock()
    bundle.id = 101
    bundle.title = "Fresh Bakery Bag"
    bundle.available = 5
    bundle.price = 3.50
    bundle.is_active = True
    return bundle

@pytest.fixture
def mock_reservation():
    """Generic Reservation Mock: Customize claim_code and status."""
    res = MagicMock()
    res.id = 501
    res.claim_code = "SAVE12"
    res.status = "RESERVED"
    res.pickup_end = datetime.now() + timedelta(hours=2)
    return res

@pytest.fixture
def mock_badge():
    """Generic Badge Mock for rewards testing."""
    badge = MagicMock()
    badge.id = 1
    badge.name = "Eco Warrior"
    badge.threshold = 5
    return badge