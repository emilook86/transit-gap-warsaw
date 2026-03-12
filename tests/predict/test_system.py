import pytest
from unittest.mock import patch
from scripts.predict import main
from src.config import OCHOTA_BOUNDS


def test_wrong_values_of_params():
    with patch(
        "sys.argv",
        [
            "predict.py",
            str(OCHOTA_BOUNDS["min_lat"] - 0.01),
            str(OCHOTA_BOUNDS["max_lon"]),
        ],
    ):
        with pytest.raises(SystemExit):
            main()


def test_wrong_number_of_params():
    with patch(
        "sys.argv",
        ["predict.py", str((OCHOTA_BOUNDS["min_lat"] + OCHOTA_BOUNDS["max_lat"]) / 2)],
    ):
        with pytest.raises(SystemExit):
            main()


def test_if_sample_boundary_works():
    with patch(
        "sys.argv",
        [
            "predict.py",
            str((OCHOTA_BOUNDS["min_lat"] + OCHOTA_BOUNDS["max_lat"]) / 2),
            str((OCHOTA_BOUNDS["min_lon"] + OCHOTA_BOUNDS["max_lon"]) / 2),
        ],
    ):
        result = main()
        assert result is None
