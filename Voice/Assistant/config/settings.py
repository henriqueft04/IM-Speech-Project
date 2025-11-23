"""
Application configuration and constants.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Selenium configuration
SELENIUM_TIMEOUT = 10  # Default wait timeout in seconds
SELENIUM_POLL_FREQUENCY = 0.5  # Poll frequency for waits
MAX_RETRY_ATTEMPTS = 3  # Retry attempts for transient failures

# NLU confidence thresholds
HIGH_CONFIDENCE_THRESHOLD = 0.80  # Execute directly
MEDIUM_CONFIDENCE_THRESHOLD = 0.60  # Ask for confirmation
LOW_CONFIDENCE_THRESHOLD = 0.45  # Minimum to process

# Intent confirmation requirements (action-specific)
REQUIRES_CONFIRMATION = {
    "search_location": False,
    "get_directions": False,
    "start_navigation": True,  # Confirm before starting nav
    "zoom_in": False,
    "zoom_out": False,
    "change_map_type": False,
    "show_traffic": False,
    "show_place_details": False,
    "show_reviews": False,
    "show_photos": False,
    "recenter_map": False,
}

# Chrome profile path (customize for your system)
# Set to None to use temporary profile
CHROME_PROFILE_PATH = None  # e.g., "~/.config/google-chrome/Default"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# WebSocket configuration (from your existing main.py)
MMI_URL = "wss://127.0.0.1:8005/IM/USER1/APP"
