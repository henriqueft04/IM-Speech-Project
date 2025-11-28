"""
Application configuration and constants.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

SELENIUM_TIMEOUT = 10
SELENIUM_POLL_FREQUENCY = 0.5
MAX_RETRY_ATTEMPTS = 3

HIGH_CONFIDENCE_THRESHOLD = 0.80
MEDIUM_CONFIDENCE_THRESHOLD = 0.60
LOW_CONFIDENCE_THRESHOLD = 0.45

REQUIRES_CONFIRMATION = {
    "search_location": False,
    "get_directions": False,
    "start_navigation": True,
    "zoom_in": False,
    "zoom_out": False,
    "change_map_type": False,
    "show_traffic": False,
    "show_place_details": False,
    "show_reviews": False,
    "show_photos": False,
    "recenter_map": False,
}

CHROME_PROFILE_PATH = None

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

MMI_URL = "wss://127.0.0.1:8005/IM/USER1/APP"
