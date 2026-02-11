import pytest

from app.services import consumer as consumer_service

def test_consumer_creation(mock_db, sample_consumer):
    # Create a new consumer using the sample data
    new_consumer = consumer_service.create_new_consumer(
        db=mock_db, 
        username=sample_consumer["username"],
        display_name=sample_consumer["display_name"],
        password=sample_consumer["password"]
    )
    
    # Assertions to verify the consumer was created correctly
    assert new_consumer is not None
    assert new_consumer.name == sample_consumer["name"]
    assert new_consumer.email == sample_consumer["email"]


    #Tests that a consumer with no display name cannot be created
    with pytest.raises(ValueError):
        new_consumer = consumer_service.create_new_consumer(
        db=mock_db, 
        username=sample_consumer["username"],
        display_name=None,
        password=sample_consumer["password"]
    )
    
    #Tests that a consumer with an empty email cannot be created
    with pytest.raises(ValueError):
        new_consumer = consumer_service.create_new_consumer(
        db=mock_db, 
        username=None,
        display_name=sample_consumer["display_name"],
        password=sample_consumer["password"]
    )
#Tests that a consumer with an username and display name that already exists cannot be created
    
    with pytest.raises(ValueError):
        new_consumer = consumer_service.create_new_consumer(
        db=mock_db, 
        username=sample_consumer["username"],
        display_name=sample_consumer["display_name"],
        password=sample_consumer["password"]
    )
    
#tests that streak is correctly checked and updated
def test_check_streak(mock_db, sample_consumer):
    # Create a new consumer using the sample data
    new_consumer = consumer_service.create_new_consumer(
        db=mock_db, 
        username=sample_consumer["username"],
        display_name=sample_consumer["display_name"],
        password=sample_consumer["password"]
    )
    
    # TODO Simulate the consumer making purchases on consecutive days
   
    
    # Retrieve the updated consumer from the database
    updated_consumer = consumer_service.get_consumer_by_id(consumer_id=new_consumer.id, db=mock_db)
    
    # Assertions to verify the streak was updated correctly
    
    #TODO boundary test on the streaks, eg. check that the streak resets after a day of inactivity and that it does not reset if the consumer makes a purchase the next day
    #TODO test that only consumers can accsess their own data and that they cannot accsess other consumers data