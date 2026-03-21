import logging
import pandas as pd
from typing import Tuple

from src.config import OCHOTA_BOUNDS

log = logging.getLogger("src.data.validation")


class DataValidationError(Exception):
    pass


def validate_stops(df: pd.DataFrame) -> pd.DataFrame:
    """Validate GTFS stops data."""
    required = {"stop_id", "stop_name", "stop_lat", "stop_lon"}
    missing = required - set(df.columns)
    if missing:
        raise DataValidationError(f"Missing columns: {missing}")

    boolean_nulls_df = df[list(required)].isnull()
    nulls_series = boolean_nulls_df.sum()
    if nulls_series.any():
        raise DataValidationError(f"Null values:\n{nulls_series[nulls_series > 0]}")

    log.info(f"Stops validation passed: {len(df)} rows")
    return df


def validate_city_name(df: pd.DataFrame) -> pd.DataFrame:
    """Validate that it is a Warsaw stop."""
    if "town_name" in df.columns:
        towns = df["town_name"].astype(str).str.strip().str.lower()
        towns = towns.replace("nan", pd.NA)

        valid_mask = (towns == "warszawa") | towns.isna()

        if not valid_mask.all():
            invalid_rows = df[~valid_mask]
            raise DataValidationError(
                f"Found {len(invalid_rows)} rows with non-Warsaw towns: {invalid_rows['town_name'].tolist()}"
            )

    log.info(f"Warsaw bus stops passed: {len(df)} rows")
    return df


def validate_amenity_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate collected amenity data."""
    count_cols = [c for c in df.columns if c.endswith("_count")]

    if not count_cols:
        raise DataValidationError("No _count columns found")

    for col in count_cols:
        if (df[col] < 0).any():
            raise DataValidationError(f"Negative values in {col}")

    log.info(f"Amenity validation passed: {len(df)} rows")
    return df


def validate_coordinates(lat: float, lon: float) -> Tuple[bool, str]:
    """Validate if coordinates are within Ochota bounds."""
    if lat <= OCHOTA_BOUNDS["min_lat"]:
        return (
            False,
            f"Latitude {lat:.6f} is too small (must be > {OCHOTA_BOUNDS['min_lat']})",
        )
    if lat >= OCHOTA_BOUNDS["max_lat"]:
        return (
            False,
            f"Latitude {lat:.6f} is too large (must be < {OCHOTA_BOUNDS['max_lat']})",
        )
    if lon <= OCHOTA_BOUNDS["min_lon"]:
        return (
            False,
            f"Longitude {lon:.6f} is too small (must be > {OCHOTA_BOUNDS['min_lon']})",
        )
    if lon >= OCHOTA_BOUNDS["max_lon"]:
        return (
            False,
            f"Longitude {lon:.6f} is too large (must be < {OCHOTA_BOUNDS['max_lon']})",
        )
    return True, ""
