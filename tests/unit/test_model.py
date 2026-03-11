import pytest
import pandas as pd

from src.features.engineering import prepare_model_data
from src.models.train import train_model


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "stop_lat": [52.2, 52.3] * 50,
            "stop_lon": [20.9, 21] * 50,
            "shop_related_count": [5, 15] * 50,
            "hospital_related_count": [6, 14] * 50,
            "school_related_count": [4, 17] * 50,
            "cube_stop_lat": [52.2**3, 52.3**3] * 50,
            "cube_stop_lon": [20.9**3, 21**3] * 50,
            "all_amenities_count": [15, 46] * 50,
        }
    )


def test_train_returns_metrics(sample_data):
    X, y = prepare_model_data(sample_data)
    _, metrics = train_model(X, y)

    assert "accuracy" in metrics
    assert "f1" in metrics
    assert 0 <= metrics["accuracy"]
    assert metrics["accuracy"] <= 1


def test_predictions_are_binary(sample_data):
    X, y = prepare_model_data(sample_data)
    model, _ = train_model(X, y)
    preds = model.predict(X)
    assert set(preds).issubset({0, 1})
