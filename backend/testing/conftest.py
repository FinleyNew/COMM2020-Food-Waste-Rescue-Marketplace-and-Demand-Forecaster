import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone
import sys
import os

# Adds the 'backend' directory to the path automatically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_db():
    """Centralized Mock Database Session."""
    db = MagicMock()
    # Default behaviors to prevent crashes
    db.commit.return_value = None
    db.add.return_value = None
    db.refresh.return_value = None
    return db

