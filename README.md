# transit-gap-warsaw
Transit Gap Warsaw Project

The goal of the project is to predict whether a given place in Ochota District of Warsaw provides a proper access to shops, schools and hospitals.

Data source: ZTM Warszawa. GTFS prepared by Mikołaj Kuranowski. Bus shapes OpenStreetMap contributors (ODbL). https://mkuran.pl/gtfs/

## Setup

1. Clone the repositorium.

2. Install uv if it not yet installed (check: https://docs.astral.sh/uv/ for installation instructions).

3. Use command "uv sync" inside the cloned repo and activate the venv:

- on macOS/Linux: "source .venv/bin/activate"

- on Windows: ".venv\Scripts\Activate.ps1"

## Instructions

1. Check out the coordinates of the place you want to search (for example from here: https://www.latlong.net/
convert-address-to-lat-long.html).

2. Run the command "uv run scripts/predict.py <LAT_COORDINATE> <LON_COORDINATE>" to find out whether there are lots of schools, shops and hospitals around that place. You can add the flag "--help" for instructions, and "--details" for more details.
