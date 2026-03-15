import pandas as pd
from src.features.engineering import (
    create_features,
    create_gap_label,
)


def test_create_features_adds_columns():
    df = pd.DataFrame(
        {
            "stop_lat": [2, 0],
            "stop_lon": [1, 0],
            "school_related_count": [6, 7],
            "hospital_related_count": [3, 5],
            "shop_related_count": [10, 10],
        }
    )
    result = create_features(df)
    assert "cube_stop_lat" in result.columns
    assert "cube_stop_lon" in result.columns
    assert "lat_times_lon" in result.columns


def test_target_when_no_amenity():
    df = pd.DataFrame(
        {
            "school_related_count": [6, 7],
            "hospital_related_count": [3, 5],
            "shop_related_count": [10, 10],
        }
    )
    result = create_gap_label(df)
    assert result["target"].iloc[0] == 0
    assert result["target"].iloc[1] == 1


def test_create_features_no_mutation():
    """Original DataFrame should not be modified."""
    df = pd.DataFrame(
        {
            "stop_lat": [51, 51.01],
            "stop_lon": [20, 20.01],
            "school_related_count": [6, 7],
            "hospital_related_count": [3, 5],
            "shop_related_count": [10, 10],
        }
    )
    original_cols = df.columns.tolist()
    _ = create_features(df)
    assert df.columns.tolist() == original_cols
