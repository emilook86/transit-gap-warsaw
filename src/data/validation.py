import logging
import pandas as pd

log = logging.getLogger("transit_gap.data.validation")


class DataValidationError(Exception):
    pass


def validate_stops(df) -> pd.DataFrame:
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


def validate_amenity_data(df) -> pd.DataFrame:
    """Validate collected amenity data."""
    count_cols = [c for c in df.columns if c.endswith("_count")]

    if not count_cols:
        raise DataValidationError("No _count columns found")

    for col in count_cols:
        if (df[col] < 0).any():
            raise DataValidationError(f"Negative values in {col}")

    log.info(f"Amenity validation passed: {len(df)} rows")
    return df
