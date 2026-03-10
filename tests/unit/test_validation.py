import pytest
import pandas as pd
from src.data.validation import (
    validate_stops,
    validate_city_name,
    validate_amenity_data,
    DataValidationError,
)

VALID_STOP_DF = pd.DataFrame(
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

VALID_AMENITY_STOP_DF = pd.DataFrame(
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


def test_valid_stops_passes():
    df = VALID_STOP_DF.copy()
    result = validate_stops(df)
    assert len(result) == 2


def test_missing_column_raises():
    df = pd.DataFrame({"stop_id": [1], "stop_lat": [52.22]})
    with pytest.raises(DataValidationError):
        validate_stops(df)


def test_if_bus_in_warsaw():
    df = VALID_STOP_DF.copy()
    validate_city_name(df)


def test_non_warsaw_stop():
    df = pd.DataFrame({"stop_id": [2], "town_name": ["Niewarszawa"]})
    with pytest.raises(DataValidationError):
        validate_city_name(df)


def test_amenity():
    df = VALID_AMENITY_STOP_DF.copy()
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
