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


    #Teests that a bundle with negative price cannot be made
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
    