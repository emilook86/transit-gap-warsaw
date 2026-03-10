import pandas as pd
import logging

from src.config import AMENITY_TAGS

log = logging.getLogger("transit_gap.features")

def create_gap_label(df, output_path) -> pd.DataFrame:
    """Create target: target = 1 if there are at least 5 amenities of each type."""

    df = df.copy()
    essential_cols = [f"{tag}_count" for tag in AMENITY_TAGS]
    
    df["target"] = 1
    for count_col in essential_cols:
        df.loc[df[count_col] < 5, "target"] = 0

    df.to_csv(output_path, index=False)
    log.info(f"Gap distribution: {df['target'].value_counts().to_dict()}")
    return df
