import pytest
from unittest.mock import MagicMock
from app.services import bundlePosting as bundles
from app.schemas.bundlePosting import BundlePostingCreate

def test_bundle_service_logic_without_db():
    """
    This test works regardless of database errors because it 
    mocks the 'db' object entirely.
    """
    # 1. Create a fake database session
    mock_db = MagicMock()

    # 2. Define what the 'fake' database should return when queried
    # We create a fake bundle object that looks like your model
    fake_bundle = MagicMock()
    fake_bundle.id = 101
    fake_bundle.description = "Mock Bread"
    fake_bundle.available_quantity = 2
    
    # When the service calls db.exec() or db.query(), return our fake bundle
    mock_db.exec.return_value.all.return_value = [fake_bundle]
    mock_db.scalar.return_value = fake_bundle

    # 3. RUN THE SERVICE: Pass the mock_db instead of a real session
    active_bundles = bundles.get_active_bundle_postings(db=mock_db)

    # 4. ASSERT: Check if the service logic processed the fake data
    assert len(active_bundles) == 1
    assert active_bundles[0].description == "Mock Bread"
    print("\n[SUCCESS] Service logic validated using a Pure Mock!")