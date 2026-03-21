import pandas as pd
import logging
from typing import Tuple

from src.config import AMENITY_TAGS, MIN_NUMBER_OF_AMENITIES_FOR_TRUE

log = logging.getLogger("src.features.engineering")


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Creates additional features: cube of both latitude and longitude, and sum of all amenities."""
    df = df.copy()
    df["sq_stop_lat"] = df["stop_lat"] ** 2
    df["sq_stop_lon"] = df["stop_lon"] ** 2
    df["lat_times_lon"] = df["stop_lat"] * df["stop_lon"]
    df["cube_stop_lat"] = df["stop_lat"] ** 3
    df["cube_stop_lon"] = df["stop_lon"] ** 3

    log.info(
        "Created columns: 'sq_stop_lat', 'sq_stop_lon', 'lat_times_lon', cube_stop_lat' and 'cube_stop_lon'"
    )

    return df


def create_gap_label(df: pd.DataFrame) -> pd.DataFrame:
    """Create target: target = 1 if there are at least MIN_NUMBER_OF_AMENITIES_FOR_TRUE amenities of each type."""

    df = df.copy()
    essential_cols = [f"{tag}_count" for tag in AMENITY_TAGS]

    df["target"] = 1
    for count_col in essential_cols:
        df.loc[df[count_col] < MIN_NUMBER_OF_AMENITIES_FOR_TRUE, "target"] = 0

    log.info(f"Gap distribution: {df['target'].value_counts().to_dict()}")
    return df


def prepare_model_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepare X, y for modeling."""
    if "lat_times_lon" not in df.columns:
        df = create_features(df)
    if "target" not in df.columns:
        df = create_gap_label(df)

    feature_cols = [
        "stop_lat",
        "stop_lon",
        "sq_stop_lat",
        "sq_stop_lon",
        "lat_times_lon",
        "cube_stop_lat",
        "cube_stop_lon",
    ]

    return df[feature_cols], df["target"]
