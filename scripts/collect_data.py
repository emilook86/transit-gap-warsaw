import logging
import pandas as pd
from src.data.osm_collector import collect_data_for_stops


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

log = logging.getLogger("collect_data")


def main():
    stops = pd.read_csv("data/processed/ochota_stops.csv")
    log.info(f"Loaded {len(stops)} stops")

    df = collect_data_for_stops(
        stops,
        output_path="data/processed/ochota_stops_with_amenities.csv",
        save_every=10,
    )

    log.info(f"\nResult:\n{df.head()}")


if __name__ == "__main__":
    main()
