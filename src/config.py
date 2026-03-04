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

# Amenities to be found

AMENITY_TAGS = {
    "shop_related": {"shop": ["supermarket", "grocery", "mall", "cosmetics", "books", "bakery"]},
    "hospital_related": {"amenity": ["hospital", "veterinary", "nursing_home", "pharmacy", "doctors", "clinic", "dentist"]},
    "school_related": {"amenity": ["kindergarten", "school", "college", "university", "music_school", "dancing_school"]},
}

# Model Constants

RANDOM_SEED = 42
TEST_SIZE = 0.3


if __name__ == "__main__":
    print(f"The project dir is: {PROJECT_ROOT}")
