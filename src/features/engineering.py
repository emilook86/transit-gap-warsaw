import pandas as pd
import logging

from src.config import AMENITY_TAGS, MIN_NUMBER_OF_AMENITIES_FOR_TRUE

log = logging.getLogger("src.features.engineering")


def create_features(df) -> pd.DataFrame:
    """Creates additional features: cube of both latitude and longitude, and sum of all amenities."""
    df = df.copy()
    df["cube_stop_lat"] = df["stop_lat"] ** 3
    df["cube_stop_lon"] = df["stop_lon"] ** 3
    df["all_amenities_count"] = (
        df["shop_related_count"]
        + df["hospital_related_count"]
        + df["school_related_count"]
    )

    log.info(
        "Created columns: 'cube_stop_lat', 'cube_stop_lon', 'all_amenities_count'."
    )

    return df


def create_gap_label(df) -> pd.DataFrame:
    """Create target: target = 1 if there are at least MIN_NUMBER_OF_AMENITIES_FOR_TRUE amenities of each type."""

    df = df.copy()
    essential_cols = [f"{tag}_count" for tag in AMENITY_TAGS]

    df["target"] = 1
    for count_col in essential_cols:
        df.loc[df[count_col] < MIN_NUMBER_OF_AMENITIES_FOR_TRUE, "target"] = 0

    log.info(f"Gap distribution: {df['target'].value_counts().to_dict()}")
    return df


def prepare_model_data(df) -> tuple[pd.DataFrame, pd.Series]:
    """Prepare X, y for modeling."""
    if "all_amenities_count" not in df.columns:
        df = create_features(df)
    if "target" not in df.columns:
        df = create_gap_label(df)

    feature_cols = [
        "stop_lat",
        "stop_lon",
        "shop_related_count",
        "hospital_related_count",
        "school_related_count",
        "cube_stop_lat",
        "cube_stop_lon",
        "all_amenities_count",
    ]

    return df[feature_cols], df["target"]
