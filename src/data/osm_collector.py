import time
import logging
import osmnx as ox
import pandas as pd
from tqdm import tqdm
from src.config import AMENITY_TAGS, WALKING_RADIUS_METERS

log = logging.getLogger("osm_collector")

ox.settings.log_console = False
ox.settings.use_cache = True
ox.settings.cache_folder = "data/cache/osm"
ox.settings.timeout = 30


class RateLimiter:
    """Prevents overwhelming OSM servers."""

    def __init__(self, delay=1):
        self.delay = delay
        self.last_request_time = None
        self.request_count = 0

    def wait(self):
        if self.last_request_time is not None:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
        self.request_count += 1


base_limiter = RateLimiter(delay=1)


def get_amenity_count(
    lat,
    lon,
    tags=AMENITY_TAGS,
    radius=WALKING_RADIUS_METERS,
    limiter: None | RateLimiter = None,
    max_retries=5,
    base_delay=0.5,
) -> int:
    """Get counts for all amenity types at a location."""

    for attempt in range(max_retries):
        try:
            if limiter:
                limiter.wait()

            amenities = ox.features_from_point((lat, lon), tags=tags, dist=radius)
            return len(amenities)

        except ox._errors.InsufficientResponseError:
            return 0

        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (3**attempt)
                log.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s")
                time.sleep(delay)
            else:
                log.error(f"All {max_retries} attempts failed: {e}")
                return 0


def get_all_amenity_counts(lat, lon) -> dict:
    """Get shop / hospital / school counts for a single location.

    Returns a dict with keys:
        shop_related_count, hospital_related_count, school_related_count
    """
    results = {}
    for amenity_type, tags in AMENITY_TAGS.items():
        count = get_amenity_count(lat, lon, tags=tags, limiter=base_limiter)
        results[f"{amenity_type}_count"] = count
    return results


def collect_data_for_stops(stops_df, output_path, save_every=10) -> pd.DataFrame:
    """Collect amenity data for all stops. Saves progress periodically."""
    results = []

    for idx, row in tqdm(stops_df.iterrows(), total=len(stops_df)):
        stop_data = {
            "stop_id": row["stop_id"],
            "stop_name": row.get("stop_name", ""),
            "stop_lat": row["stop_lat"],
            "stop_lon": row["stop_lon"],
        }

        amenities = get_all_amenity_counts(row["stop_lat"], row["stop_lon"])
        stop_data.update(amenities)
        results.append(stop_data)

        if (idx + 1) % save_every == 0:
            pd.DataFrame(results).to_csv(output_path, index=False)
            log.info(f"Progress saved: {idx + 1}/{len(stops_df)}")

    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)
    log.info(f"Complete! Saved {len(df)} stops to {output_path}")
    return df
