import logging
import pandas as pd
from src.data.osm_collector import collect_data_for_stops
from src.config import DATA_PROCESSED, LOG_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "collect_data.log"),
        logging.StreamHandler(),
    ],
)

log = logging.getLogger("collect_data")


def main():
    log.info("=== START ===")
    stops = pd.read_csv(DATA_PROCESSED / "ochota_stops.csv")
    log.info(f"Loaded {len(stops)} stops")

    df = collect_data_for_stops(
        stops,
        output_path=DATA_PROCESSED/"ochota_stops_with_amenities.csv",
        save_every=10,
    )

    log.info("Result:")
    log.info(df.head())
    log.info("=== END ===")


if __name__ == "__main__":
    main()
