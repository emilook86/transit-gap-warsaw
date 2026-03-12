import pytest
import pandas as pd
from src.data.validation import (
    validate_stops,
    validate_city_name,
    validate_amenity_data,
    validate_coordinates,
    DataValidationError,
)
from src.config import OCHOTA_BOUNDS


@pytest.fixture
def sample_valid_stop_df():
    return pd.DataFrame(
        {
            "stop_id": ["155243", "210593"],
            "stop_name": ["Ochota Ratusz", "Plac Narutowicza"],
            "stop_code": ["11", "12"],
            "platform_code": ["", ""],
            "stop_lat": ["52.22", "52.23"],
            "stop_lon": ["21.00", "21.01"],
            "location_type": ["0", "0"],
            "parent_station": ["", ""],
            "wheelchair_boarding": ["1", "1"],
            "zone_id": ["1", "1"],
            "stop_name_stem": ["Ochota Ratusz", "Plac Narutowicza"],
            "town_name": ["Warszawa", "Warszawa"],
            "street_name": ["Grójecka", "Grójecka"],
        }
    )


@pytest.fixture
def sample_valid_amenity_stop_df():
    return pd.DataFrame(
        {
            "stop_id": ["155243", "210593"],
            "stop_name": ["Ochota Ratusz", "Plac Narutowicza"],
            "stop_lat": ["52.22", "52.23"],
            "stop_lon": ["21.00", "21.01"],
            "shop_related_count": [5, 8],
            "hospital_related_count": [2, 11],
            "school_related_count": [3, 16],
        }
    )


def test_valid_stops_passes(sample_valid_stop_df):
    df = sample_valid_stop_df.copy()
    result = validate_stops(df)
    assert len(result) == 2


def test_missing_column_raises():
    df = pd.DataFrame({"stop_id": [1], "stop_lat": [52.22]})
    with pytest.raises(DataValidationError):
        validate_stops(df)


def test_if_bus_in_warsaw(sample_valid_stop_df):
    df = sample_valid_stop_df.copy()
    validate_city_name(df)


def test_non_warsaw_stop():
    df = pd.DataFrame({"stop_id": [2], "town_name": ["Niewarszawa"]})
    with pytest.raises(DataValidationError):
        validate_city_name(df)


def test_amenity(sample_valid_amenity_stop_df):
    df = sample_valid_amenity_stop_df.copy()
    result = validate_amenity_data(df)
    assert len(result) == 2


def test_no_count():
    df = pd.DataFrame({"stop_id": [3]})
    with pytest.raises(DataValidationError):
        validate_amenity_data(df)


def test_negative_count():
    df = pd.DataFrame(
        {"stop_id": [4], "shop_related_count": [1], "school_related_count": [-3]}
    )
    with pytest.raises(DataValidationError):
        validate_amenity_data(df)


@pytest.fixture
def mean_coordinates():
    mean_lat = (OCHOTA_BOUNDS["min_lat"] + OCHOTA_BOUNDS["max_lat"]) / 2
    mean_lon = (OCHOTA_BOUNDS["min_lon"] + OCHOTA_BOUNDS["max_lon"]) / 2
    return mean_lat, mean_lon


def test_validate_correct_coordinates(mean_coordinates):
    result, _ = validate_coordinates(*mean_coordinates)
    assert result is True


def test_validate_coordinates_lat_too_small(mean_coordinates):
    result, message = validate_coordinates(
        OCHOTA_BOUNDS["min_lat"] - 0.01, mean_coordinates[1]
    )
    assert result is False
    assert "Latitude" in message and "too small" in message


def test_validate_coordinates_lon_too_large(mean_coordinates):
    result, message = validate_coordinates(
        mean_coordinates[0], OCHOTA_BOUNDS["max_lon"]
    )
    assert result is False
    assert "Longitude" in message and "too large" in message
