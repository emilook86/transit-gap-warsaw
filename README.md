# Transit Gap Ochota District

A lightweight CLI tool that predicts whether there are enough schools, hospitals, and shops within walking distance of any location in Warsaw's Ochota district.

## Requirements

- [uv](https://docs.astral.sh/uv/) package manager
- Linux, macOS, or Windows

## Quick Start

```bash
# Installation
git clone https://github.com/emilook86/transit-gap-warsaw.git
cd transit-gap-warsaw
uv sync

# Activate environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\Activate.ps1

# Run prediction (default: 5 amenities within 500m)
uv run scripts/predict.py <LATITUDE> <LONGITUDE>
```

## Usage Examples

Click [here](https://www.latlong.net/convert-address-to-lat-long.html) in order to easily check coordinates of a given place on the map.

```bash
# Basic prediction
uv run scripts/predict.py 52.215 20.97

# Details mode - shows actual counts and verifies prediction
uv run scripts/predict.py --details 52.21 20.96

# Show help
uv run scripts/predict.py --help
```

## Configuration

Edit `src/config.py` to modify defaults:

- `WALKING_RADIUS_METERS = 500`
- `MIN_NUMBER_OF_AMENITIES_FOR_TRUE = 5`

## Documentation

Detailed project documentation is available in the repository can be found under [docs/transit_gap_documentation.pdf](https://github.com/emilook86/transit-gap-warsaw/blob/main/docs/transit_gap_documentation.pdf).

## Data Sources

- **GTFS data**: ZTM Warszawa, prepared by Mikołaj Kuranowski
- **Amenities**: OpenStreetMap contributors (ODbL)
- **License**: MIT
