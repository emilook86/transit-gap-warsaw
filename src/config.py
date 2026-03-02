from pathlib import Path

# Paths

PROJECT_ROOT = Path.cwd()
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

# Warsaw Bounds

WARSAW_BOUNDS = {
    "min_lat": 52.12, # south
    "max_lat": 52.33, # north
    "min_lon": 20.85, # west
    "max_lon": 21.18 # east
}

# Model Constants

RANDOM_SEED = 42
TEST_SIZE = 0.3
