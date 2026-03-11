from pathlib import Path
import logging

# Paths

PROJECT_ROOT = Path.cwd()
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "artifacts" / "models"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
LOG_DIR = PROJECT_ROOT / "artifacts" / "logs"

# Ochota District Bounds

OCHOTA_BOUNDS = {
    "min_lat": 52.2,  # south
    "max_lat": 52.23,  # north
    "min_lon": 20.94,  # west
    "max_lon": 21,  # east
}

# Amenities to be found

AMENITY_TAGS = {
    "shop_related": {"shop": ["supermarket", "grocery", "mall", "bakery"]},
    "hospital_related": {"amenity": ["hospital", "pharmacy", "doctors", "clinic"]},
    "school_related": {"amenity": ["kindergarten", "school", "college", "university"]},
}

WALKING_RADIUS_METERS = 500

# Model Constants

RANDOM_SEED = 42
TEST_SIZE = 0.3

# Add setup logging


def setup_logging(level: str = "INFO", log_file: Path = LOG_DIR / "scripts.log"):
    """Call this ONCE at the start of scripts."""
    logger = logging.getLogger("transit_gap")
    logger.setLevel(getattr(logging, level))

    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    # Remove console handler - only add file handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
