import logging
import pandas as pd
from src.features.engineering import (
    create_features,
    create_gap_label,
    prepare_model_data,
)
from src.models.train import train_model, save_model

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

log = logging.getLogger("train_model")


def main():
    df = pd.read_csv("data/processed/ochota_stops_with_amenities.csv")

    df = create_features(df)
    df = create_gap_label(df)

    X, y = prepare_model_data(df)
    log.info(f"Features: {X.columns.tolist()}")
    log.info(f"Target: {y.value_counts().to_dict()}")

    model, metrics = train_model(X, y)

    log.info("\nResults:\n")
    for metric, value in metrics.items():
        log.info(f"{metric}: {value:.3f}")

    save_model(model, metrics, X.columns.tolist())


if __name__ == "__main__":
    main()
