
import pytest

# Fixture for a Mock Database Session 
# (Once the DB is built, you swap this for a real SQL action) -- james
@pytest.fixture
def mock_db():
    return "Database_Connection_Placeholder"

# Fixture for a Seller 
@pytest.fixture
def sample_seller():
    return {
        "id": 1,
        "username": "Exeter_Bakery",
        "role": "seller"
    }

# Fixture for a Bundle 
@pytest.fixture
def sample_bundle():
    return {
        "id": 101,
        "title": "Evening Pastry Bag",
        "available": 5,
        "price": 3.50,
        "pickup_window": "5:30 - 6:30 PM", 
        
    }