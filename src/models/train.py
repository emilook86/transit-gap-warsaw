import json
import logging
from datetime import datetime
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
import xgboost as xgb

from src.config import RANDOM_SEED, TEST_SIZE, MODELS_DIR

log = logging.getLogger("src.models.train")


def train_model(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_SEED,
) -> tuple:
    """Train XGBoost with hyperparameter grid search, return (best_model, metrics)."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    log.info(f"Train: {len(X_train)}, Test: {len(X_test)}")

    model = xgb.XGBClassifier(random_state=random_state, eval_metric="auc")

    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [3, 4, 5],
        "learning_rate": [0.01, 0.05, 0.1],
        "min_child_weight": [1, 2, 3],
    }

    log.info("Starting grid search")
    grid_search = GridSearchCV(
        estimator=model, param_grid=param_grid, cv=5, scoring="roc_auc"
    )

    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    log.info(f"Best parameters: {grid_search.best_params_}")
    log.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")

    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_pred_proba)),
        "best_params": grid_search.best_params_,
        "best_cv_score": float(grid_search.best_score_),
    }

    cv = cross_val_score(best_model, X, y, cv=5, scoring="roc_auc")
    metrics["cv_roc_auc_mean"] = float(cv.mean())
    metrics["cv_roc_auc_std"] = float(cv.std())

    log.info(f"Test metrics: {metrics}")
    return best_model, metrics


def save_model(model, metrics: dict, features: list):
    """Save model + metadata JSON side by side."""
    path = MODELS_DIR / "xgboost_gap_model.joblib"
    path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, path)

    metadata = {
        "saved_at": datetime.now().isoformat(),
        "metrics": metrics,
        "features": features,
        "model_type": "XGBClassifier",
        "xgboost_params": model.get_params(),
    }

    meta_path = path.with_suffix(".json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2, default=str)

    log.info(f"Model saved: {path}")
    log.info(f"Metadata saved: {meta_path}")
