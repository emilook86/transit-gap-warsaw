import logging
import pandas as pd
from src.features.engineering import create_gap_label

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():
    stops = pd.read_csv("data/processed/ochota_stops_with_amenities.csv")
    print(f"Loaded {len(stops)} stops")

    df = create_gap_label(
        stops,
        output_path="data/processed/ochota_stops_with_target_var.csv",
    )
    print(f"\nResult:\n{df.head()}")


if __name__ == "__main__":
    main()
