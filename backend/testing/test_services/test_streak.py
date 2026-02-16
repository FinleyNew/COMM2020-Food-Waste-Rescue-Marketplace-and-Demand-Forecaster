import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock
from app.services import consumer as consumer_service

#simple user class to mimic a consumer to be stored in memeory
class SimpleUser:
    def __init__(self, user_id, streak):
        self.user_id = user_id
        self.streak = streak  
        self.last_activity = None

#Tests the check_streak function to ensure that it correctly resets the streak after 7 days of inactivity.

def test_streak_reset_after_7_days(mock_db):
    # Create a simpleUser with a streak of 5
    user = SimpleUser(user_id=1, streak=5)
    
    # Simulate a reservation from 10 days ago
    ten_days_ago = datetime.now(timezone.utc) - timedelta(days=10)
    old_res = MagicMock()
    old_res.timestamp = ten_days_ago
    old_res.status = "COLLECTED"

    #Ensure the .get returns the user when the service tries to retrieve it
    mock_db.get.return_value = user
    
    
    # Ensures when the mock database is used in the CRUD it returns the user and the old reservation
    chain_mock = mock_db.exec.return_value
    chain_mock.where.return_value = chain_mock
    chain_mock.one.return_value = user
    chain_mock.all.return_value = [old_res]

    
    consumer_service.check_streak(consumer_id=1, db=mock_db)
        
   
    assert user.streak == 0

def test_streak_persists_when_active(mock_db):
    # Create a user with a streak and a recent reservation
    user = SimpleUser(user_id=1, streak=5)
    recent_time = datetime.now(timezone.utc) - timedelta(days=1)
    
    recent_res = MagicMock()
    recent_res.timestamp = recent_time
    recent_res.status = "COLLECTED"
    
    #Ensure the .get returns the user when the service tries to retrieve it
    mock_db.get.return_value = user
    chain_mock = mock_db.exec.return_value
    chain_mock.where.return_value = chain_mock
    chain_mock.one.return_value = user
    chain_mock.all.return_value = [recent_res]

    
    consumer_service.check_streak(consumer_id=1, db=mock_db)

    
    assert user.streak == 5
def test_no_reservations(mock_db):
    # Create a user with no reservations
    user = SimpleUser(user_id=1, streak=5)
    
    #Ensure the .get returns the user when the service tries to retrieve it
    mock_db.get.return_value = user
    chain_mock = mock_db.exec.return_value
    chain_mock.where.return_value = chain_mock
    chain_mock.one.return_value = user
    chain_mock.all.return_value = []  # No reservations

    
    with pytest.raises(Exception): # Expect an error because there are no reservations
        consumer_service.check_streak(consumer_id=1, db=mock_db)
