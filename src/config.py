from pathlib import Path

# Paths

PROJECT_ROOT = Path.cwd()
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

# Ochota District Bounds

OCHOTA_BOUNDS = {
    "min_lat": 52.2,  # south
    "max_lat": 52.23,  # north
    "min_lon": 20.94,  # west
    "max_lon": 21,  # east
}

# Model Constants

RANDOM_SEED = 42
TEST_SIZE = 0.3


if __name__ == "__main__":
    print(f"The project dir is: {PROJECT_ROOT}")
