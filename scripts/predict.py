import argparse
import sys
from pathlib import Path
import pandas as pd
import joblib
import logging

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import (
    AMENITY_TAGS,
    OCHOTA_BOUNDS,
    WALKING_RADIUS_METERS,
    MIN_NUMBER_OF_AMENITIES_FOR_TRUE,
    MODELS_DIR,
    LOG_DIR,
)
from src.data.osm_collector import get_all_amenity_counts
from src.data.validation import validate_coordinates
from src.features.engineering import (
    create_features,
    create_gap_label,
    prepare_model_data,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "predict.log"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("src.data.validation").setLevel(logging.WARNING)
logging.getLogger("src.features.engineering").setLevel(logging.WARNING)
log = logging.getLogger("predict")
model = joblib.load(MODELS_DIR / "xgboost_gap_model.joblib")


def main():
    description = f"Predict transit gap for a location in Ochota District of Warsaw. \
        The application checks if there are at least {MIN_NUMBER_OF_AMENITIES_FOR_TRUE} \
        buildings of school, shop and hospital (of each cathegory) in the {WALKING_RADIUS_METERS} meters \
        around the provided geolocation. \
        Provide two argumeters: first latitude, then longitude. \
        There are following restrictions: \
        Latitude should be greater than {OCHOTA_BOUNDS['min_lat']} and less than {OCHOTA_BOUNDS['max_lat']}. \
        Longitude should be greater than {OCHOTA_BOUNDS['min_lon']} and less than {OCHOTA_BOUNDS['max_lon']}."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("lat", type=float, help="Latitude (e.g., 52.2297)")
    parser.add_argument("lon", type=float, help="Longitude (e.g., 20.9922)")
    parser.add_argument(
        "--details",
        action="store_true",
        help="Find if the model actually predicts right the transit gap. \
            Specifies exact number of all amenities.",
    )

    args = parser.parse_args()

    is_valid, error_msg = validate_coordinates(args.lat, args.lon)
    if not is_valid:
        log.error(error_msg)
        log.info("Run with --help for more information")
        sys.exit(1)

    log.info(f"Checking location: {args.lat:.6f}, {args.lon:.6f}")
    log.info("Fetching data from OpenStreetMap (it might take about one minute)")

    data = {
        "stop_id": 1,
        "stop_name": "name",
        "stop_lat": args.lat,
        "stop_lon": args.lon,
    }

    try:
        results = get_all_amenity_counts(args.lat, args.lon)
        data.update(results)
        df = pd.DataFrame([data])
        df = create_features(df)
        df = create_gap_label(df)
        X, y_true = prepare_model_data(df)
        y_pred = model.predict(X)

        if y_pred == 1:
            log.info(
                "*** The place you have chosen is rich in schools, hospitals and shops ***"
            )
        else:
            log.info(
                "*** There may be lack of sufficient numbers of schools, hospitals or shops ***"
            )

        if args.details:
            log.info("Let's check, whether our prediction matches the actual target")
            if y_pred[0] == y_true[0]:
                log.info("*** It matches! The model predicted correctly ***")
            else:
                log.info("*** The model predicted wrong. What a pity! ***")

            log.info("Actual true amenity counts:")
            for name in AMENITY_TAGS.keys():
                count = results.get(f"{name}_count", 0)
                log.info(f"  {name}: {count}")

    except Exception as e:
        log.error(f"Error during prediction: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
