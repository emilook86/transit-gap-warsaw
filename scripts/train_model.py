import logging
import pandas as pd
from src.features.engineering import (
    create_features,
    create_gap_label,
    prepare_model_data,
)
from src.models.train import train_model, save_model
from src.config import DATA_PROCESSED, LOG_DIR


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "train_model.log"),
        logging.StreamHandler(),
    ],
)

log = logging.getLogger("train_model")


def main():
    log.info("=== START ===")
    df = pd.read_csv(DATA_PROCESSED / "ochota_stops_with_amenities.csv")

    df = create_features(df)
    df = create_gap_label(df)

    X, y = prepare_model_data(df)
    log.info(f"Features: {X.columns.tolist()}")
    log.info(f"Target: {y.value_counts().to_dict()}")

    model, metrics = train_model(X, y)

    log.info("Results:")
    for metric, value in metrics.items():
        log.info(f"{metric}: {value:.3f}")

    save_model(model, metrics, X.columns.tolist())
    log.info("=== END ===")


if __name__ == "__main__":
    main()
