import pytest
from app.services import bundles 


def test_bundle_creation(mock_db, sample_seller, sample_bundle):
    # Initialize the BundleService with the mock database
    
    
    # Create a new bundle using the sample data
    created_bundle = bundles.create_bundle(
        seller_id=sample_seller["id"],
        title=sample_bundle["title"],
        available=sample_bundle["available"],
        price=sample_bundle["price"]
    )
    
    # Assertions to verify the bundle was created correctly
    assert created_bundle is not None
    assert created_bundle.title == sample_bundle["title"]
    assert created_bundle.available == sample_bundle["available"]
    assert created_bundle.price == sample_bundle["price"]


    #Tests that a bundle with negative price cannot be made
    with pytest.raises(ValueError):
        bundles.create_bundle(
            seller_id=sample_seller["id"],
            title=sample_bundle["title"],
            available=sample_bundle["available"],
            price=-10
    )
        #Tests that a bundle with zero price can be made (free bundle)
        bundles.create_bundle(
            seller_id=sample_seller["id"],
            title=sample_bundle["title"],
            available=sample_bundle["available"],
            price= 0
        )
        #TODO tests bundle set to be picked up in the past
        bundles.create_bundle(
            seller_id=sample_seller["id"],
            title=sample_bundle["title"],
            available=sample_bundle["available"],
            price=sample_bundle["price"],
            pickup_time="2020-01-01T10:00:00Z"  # Past date
        )


def test_bundle_retrieval(mock_db, sample_seller, sample_bundle):
    # Create a bundle to retrieve
    created_bundle = bundles.create_bundle(
        seller_id=sample_seller["id"],
        title=sample_bundle["title"],
        available=sample_bundle["available"],
        price=sample_bundle["price"]
    )
    
    # Retrieve the bundle by its ID
    retrieved_bundle = bundles.get_bundle_by_id(created_bundle.id)
    
    # Assertions to verify the retrieved bundle matches the created one
    assert retrieved_bundle is not None
    assert retrieved_bundle.id == created_bundle.id
    assert retrieved_bundle.title == created_bundle.title
    assert retrieved_bundle.available == created_bundle.available
    assert retrieved_bundle.price == created_bundle.price

def test_bundle_update(mock_db, sample_seller, sample_bundle):
    # Create a bundle to update
    created_bundle = bundles.create_bundle(
        seller_id=sample_seller["id"],
        title=sample_bundle["title"],
        available=sample_bundle["available"],
        price=sample_bundle["price"]
    )
    
    # Update the bundle's title and price
    updated_title = "Updated Bundle Title"
    updated_price = 19.99
    updated_bundle = bundles.update_bundle(
        bundle_id=created_bundle.id,
        title=updated_title,
        price=updated_price
    )
    
    # Assertions to verify the bundle was updated correctly
    assert updated_bundle is not None
    assert updated_bundle.id == created_bundle.id
    assert updated_bundle.title == updated_title
    assert updated_bundle.price == updated_price
    
     #Tests that a bundle with zero price can be made (free bundle)
    with pytest.raises(ValueError):
        bundles.update_bundle(
            bundle_id=created_bundle.id,
            title=updated_title,
            price=-10)
def test_bundle_deletion(mock_db, sample_seller, sample_bundle):
    # Create a bundle to delete
    created_bundle = bundles.create_bundle(
        seller_id=sample_seller["id"],
        title=sample_bundle["title"],
        available=sample_bundle["available"],
        price=sample_bundle["price"]
    )
    
    # Delete the bundle
    deletion_result = bundles.delete_bundle(bundle_id=created_bundle.id)
    
    # Assertions to verify the bundle was deleted successfully
    assert deletion_result is True
    
    # Attempt to retrieve the deleted bundle
    retrieved_bundle = bundles.get_bundle_by_id(created_bundle.id)
    
    # Assertions to verify the bundle no longer exists
    assert retrieved_bundle is None

#TODO Attempt to delete or edit a bundle that belongs to a different seller.

#TODO Verify a bundle's status changes from Active to Expired once the pickup time passes.

#TODO Verify that only bundles with available=True are returned in the list of active bundles.

#TODO Verify that the list of active bundles does not include bundles that have already been picked up or deleted.


    