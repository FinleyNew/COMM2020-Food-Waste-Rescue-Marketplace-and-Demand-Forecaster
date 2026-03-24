"""
Tests the demand-forecasting layer: schema validation for forecast
fields, and the service functions that delegate to CRUD or orchestrate
the ML pipeline (get_forecast, create_forecast, delete_forecast).

The ML model itself (PoissonRegressor pipeline) is mocked because
unit tests should not depend on trained model weights or random state.
We verify that the service wires up the pipeline correctly and
normalises predictions (non-negative reservations, probability in [0,1]).
"""

import pytest
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch
from pydantic import ValidationError

from app.services import forecast as forecast_service
from app.schemas.forecast import ForecastCreate, ForecastPublic




@pytest.fixture
def mock_db():
    
    return MagicMock()



# ForecastBase enforces predicted_reservations >= 0 and
# predicted_no_show_prob  [0, 1].

def test_forecast_create_valid():
    # A ForecastCreate with valid predicted_reservations and predicted_no_show_prob should succeed.
    fc = ForecastCreate(
        user_id=1,
        posting_id=10,
        predicted_reservations=5,
        predicted_no_show_prob=0.2,
    )
    assert fc.predicted_reservations == 5
    assert fc.predicted_no_show_prob == 0.2


def test_forecast_create_negative_reservations_rejected():
    # predicted_reservations < 0 violates Field(ge=0). A forecast should never predict negative demand.
    with pytest.raises(ValidationError):
        ForecastCreate(
            user_id=1,
            posting_id=10,
            predicted_reservations=-1,
            predicted_no_show_prob=0.1,
        )


def test_forecast_create_no_show_over_1_rejected():
    # predicted_no_show_prob > 1.0 violates Field(le=1). Probability cannot exceed 100 %.
    with pytest.raises(ValidationError):
        ForecastCreate(
            user_id=1,
            posting_id=10,
            predicted_reservations=3,
            predicted_no_show_prob=1.5,
        )


def test_forecast_create_no_show_negative_rejected():
    # predicted_no_show_prob < 0 violates Field(ge=0). Probability cannot be negative.
    with pytest.raises(ValidationError):
        ForecastCreate(
            user_id=1,
            posting_id=10,
            predicted_reservations=3,
            predicted_no_show_prob=-0.1,
        )


def test_forecast_create_zero_reservations_accepted():
    # predicted_reservations = 0 is valid and should be accepted. A forecast of zero demand is plausible.
    fc = ForecastCreate(
        user_id=1,
        predicted_reservations=0,
        predicted_no_show_prob=0.0,
    )
    assert fc.predicted_reservations == 0




def test_get_forecast_returns_normalised_prediction(mock_db):
    # The get_forecast service should return a ForecastPublic with non-negative predicted_reservations and a predicted_no_show_prob in [0, 1]
    # This test mocks the ML pipeline to return specific values and verifies that the service normalises them correctly.
    import numpy as np
    import pandas as pd

    mock_bundle = MagicMock()
    mock_bundle.user_id = 1
    mock_bundle.category = "bakery"
    mock_bundle.price = Decimal("2.50")
    mock_bundle.start_time = datetime(2025, 6, 10, 9, 0, tzinfo=timezone.utc)
    mock_bundle.end_time = datetime(2025, 6, 10, 12, 0, tzinfo=timezone.utc)
    mock_bundle.raining = False

    # Mock the ML pipelines to return controllable numbers
    mock_res_model = MagicMock()
    mock_res_model.predict.return_value = np.array([3.7])
    mock_no_show_model = MagicMock()
    mock_no_show_model.predict.return_value = np.array([1.2])

    with patch("app.crud.record.get_all_records", return_value=[]), \
         patch("app.crud.record.get_same_time_records", return_value=[]), \
         patch("app.services.forecast.create_dataframe", return_value=pd.DataFrame()), \
         patch("app.services.forecast.train_model", return_value=(mock_res_model, mock_no_show_model)):
        result = forecast_service.get_forecast(bundle_in=mock_bundle, db=mock_db)

    assert result.predicted_reservations >= 0
    assert 0.0 <= result.predicted_no_show_prob <= 1.0
    assert result.user_id == 1


def test_get_forecast_zero_predicted_reservations_yields_zero_no_show(mock_db):
    # When the reservation model predicts 0 (or negative), no_show_prob should default to 0.0 rather than dividing by zero.
    # This verifies the y_pred_res > 0 guard in the normalisation code.
    import numpy as np
    import pandas as pd

    mock_bundle = MagicMock()
    mock_bundle.user_id = 1
    mock_bundle.category = "bakery"
    mock_bundle.price = Decimal("1.00")
    mock_bundle.start_time = datetime(2025, 6, 10, 9, 0, tzinfo=timezone.utc)
    mock_bundle.end_time = datetime(2025, 6, 10, 12, 0, tzinfo=timezone.utc)
    mock_bundle.raining = False

    mock_res_model = MagicMock()
    mock_res_model.predict.return_value = np.array([-0.5])  # negative → clamped to 0
    mock_no_show_model = MagicMock()
    mock_no_show_model.predict.return_value = np.array([0.3])

    with patch("app.crud.record.get_all_records", return_value=[]), \
         patch("app.crud.record.get_same_time_records", return_value=[]), \
         patch("app.services.forecast.create_dataframe", return_value=pd.DataFrame()), \
         patch("app.services.forecast.train_model", return_value=(mock_res_model, mock_no_show_model)):
        result = forecast_service.get_forecast(bundle_in=mock_bundle, db=mock_db)

    assert result.predicted_reservations == 0
    assert result.predicted_no_show_prob == 0.0
