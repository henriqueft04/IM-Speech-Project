"""
Selenium WebDriver configuration and management.
Provides a persistent Chrome session with Google Maps optimizations.
"""

import logging
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

logger = logging.getLogger(__name__)


class DriverConfig:
    """Configuration for Chrome WebDriver with persistent session."""

    GOOGLE_MAPS_URL = "https://www.google.com/maps"

    # Browser preferences
    PREFS = {
        "profile.default_content_setting_values.media_stream_mic": 1,  # Allow microphone
        "profile.default_content_setting_values.geolocation": 1,        # Allow location
        "profile.default_content_setting_values.notifications": 2,      # Block notifications
    }

    # Chrome arguments
    CHROME_ARGS = [
        "--disable-blink-features=AutomationControlled",  # Avoid detection
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--start-maximized",
    ]

    @classmethod
    def create_driver(
        cls,
        headless: bool = False,
        user_data_dir: Optional[str] = None
    ) -> WebDriver:
        """
        Create a configured Chrome WebDriver instance.

        Args:
            headless: Run browser in headless mode (no UI)
            user_data_dir: Path to Chrome user profile for persistent login

        Returns:
            Configured WebDriver instance
        """
        options = Options()

        # Add chrome arguments
        for arg in cls.CHROME_ARGS:
            options.add_argument(arg)

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        # Set preferences
        options.add_experimental_option("prefs", cls.PREFS)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Use persistent profile if provided
        if user_data_dir:
            user_data_path = Path(user_data_dir).expanduser()
            if user_data_path.exists():
                options.add_argument(f"--user-data-dir={user_data_path}")
                logger.info(f"Using Chrome profile: {user_data_path}")
            else:
                logger.warning(f"Profile path not found: {user_data_path}")

        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(0)  # Disable implicit waits (we use explicit)
            logger.info("Chrome WebDriver initialized successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise


class DriverManager:
    """Manages WebDriver lifecycle for persistent sessions."""

    def __init__(self, config: DriverConfig = None):
        self.config = config or DriverConfig()
        self._driver: Optional[WebDriver] = None

    @property
    def driver(self) -> WebDriver:
        """Get or create the WebDriver instance."""
        if self._driver is None:
            raise RuntimeError("Driver not initialized. Call start() first.")
        return self._driver

    def start(
        self,
        headless: bool = False,
        user_data_dir: Optional[str] = None
    ) -> WebDriver:
        """
        Start the WebDriver session.

        Args:
            headless: Run in headless mode
            user_data_dir: Chrome profile directory for persistent login

        Returns:
            WebDriver instance
        """
        if self._driver is not None:
            logger.warning("Driver already started. Returning existing instance.")
            return self._driver

        self._driver = self.config.create_driver(
            headless=headless,
            user_data_dir=user_data_dir
        )

        # Navigate to Google Maps
        self._driver.get(self.config.GOOGLE_MAPS_URL)
        logger.info(f"Navigated to {self.config.GOOGLE_MAPS_URL}")

        return self._driver

    def stop(self):
        """Stop the WebDriver session gracefully."""
        if self._driver:
            try:
                self._driver.quit()
                logger.info("WebDriver stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping WebDriver: {e}")
            finally:
                self._driver = None

    def restart(
        self,
        headless: bool = False,
        user_data_dir: Optional[str] = None
    ) -> WebDriver:
        """Restart the WebDriver session."""
        self.stop()
        return self.start(headless=headless, user_data_dir=user_data_dir)

    def is_alive(self) -> bool:
        """Check if the driver is still responsive."""
        if self._driver is None:
            return False

        try:
            # Try to get current URL as a health check
            _ = self._driver.current_url
            return True
        except Exception:
            return False

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
