"""
Base Page Object class with common functionality.
All page objects should inherit from this class.
"""

import logging
from typing import Tuple, Optional, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from infrastructure.selenium_helpers import (
    retry_on_stale_element,
    retry_on_click_intercepted,
    safe_click,
    wait_for_element,
    wait_for_element_clickable,
    wait_for_elements,
    is_element_present,
    scroll_to_element,
    ElementNotFoundException,
)
from config.settings import SELENIUM_TIMEOUT

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base page object with common Selenium operations.

    All page-specific classes should inherit from this class to get
    smart waits, retry logic, and common utilities.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize base page.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, SELENIUM_TIMEOUT)

    @retry_on_stale_element()
    def find_element(
        self,
        locator: Tuple[str, str],
        timeout: int = SELENIUM_TIMEOUT
    ) -> WebElement:
        """
        Find a single element with automatic retry on stale reference.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time

        Returns:
            WebElement

        Raises:
            ElementNotFoundException: If element not found
        """
        return wait_for_element(self.driver, locator, timeout)

    @retry_on_stale_element()
    def find_elements(
        self,
        locator: Tuple[str, str],
        timeout: int = SELENIUM_TIMEOUT
    ) -> List[WebElement]:
        """
        Find multiple elements.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time

        Returns:
            List of WebElements (empty list if none found)
        """
        return wait_for_elements(self.driver, locator, timeout)

    @retry_on_stale_element()
    @retry_on_click_intercepted()
    def click(
        self,
        locator: Tuple[str, str],
        timeout: int = SELENIUM_TIMEOUT,
        scroll_first: bool = True
    ):
        """
        Click an element with retry logic and fallback strategies.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time
            scroll_first: Scroll element into view before clicking

        Raises:
            ElementNotFoundException: If element not found
        """
        element = wait_for_element_clickable(self.driver, locator, timeout)

        if scroll_first:
            scroll_to_element(self.driver, element)

        safe_click(element, self.driver)
        logger.debug(f"Clicked element: {locator}")

    @retry_on_stale_element()
    def send_keys(
        self,
        locator: Tuple[str, str],
        text: str,
        clear_first: bool = True,
        timeout: int = SELENIUM_TIMEOUT
    ):
        """
        Send text to an input element.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            text: Text to send
            clear_first: Clear existing text before sending
            timeout: Maximum wait time
        """
        element = wait_for_element_clickable(self.driver, locator, timeout)

        if clear_first:
            element.clear()

        element.send_keys(text)
        logger.debug(f"Sent keys to {locator}: {text}")

    @retry_on_stale_element()
    def get_text(
        self,
        locator: Tuple[str, str],
        timeout: int = SELENIUM_TIMEOUT
    ) -> str:
        """
        Get text content of an element.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time

        Returns:
            Element text content
        """
        element = self.find_element(locator, timeout)
        return element.text

    @retry_on_stale_element()
    def get_attribute(
        self,
        locator: Tuple[str, str],
        attribute: str,
        timeout: int = SELENIUM_TIMEOUT
    ) -> Optional[str]:
        """
        Get attribute value of an element.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            attribute: Attribute name
            timeout: Maximum wait time

        Returns:
            Attribute value or None
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)

    def is_element_visible(
        self,
        locator: Tuple[str, str],
        timeout: int = 2
    ) -> bool:
        """
        Check if element is visible on the page.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time

        Returns:
            True if visible, False otherwise
        """
        return is_element_present(self.driver, locator, timeout)

    def wait_for_element_to_disappear(
        self,
        locator: Tuple[str, str],
        timeout: int = SELENIUM_TIMEOUT
    ) -> bool:
        """
        Wait for an element to disappear from the page.

        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Maximum wait time

        Returns:
            True if element disappeared, False otherwise
        """
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def send_keyboard_shortcut(self, *keys: str):
        """
        Send keyboard shortcut to the active element.

        Args:
            keys: Keys to send (e.g., Keys.CONTROL, 'f')
        """
        actions = ActionChains(self.driver)
        for key in keys:
            actions.key_down(key)
        for key in reversed(keys):
            actions.key_up(key)
        actions.perform()
        logger.debug(f"Sent keyboard shortcut: {keys}")

    def execute_script(self, script: str, *args) -> any:
        """
        Execute JavaScript in the browser.

        Args:
            script: JavaScript code to execute
            args: Arguments to pass to the script

        Returns:
            Script return value
        """
        return self.driver.execute_script(script, *args)

    def scroll_page(self, direction: str = "down", amount: int = 300):
        """
        Scroll the page in a given direction.

        Args:
            direction: "up" or "down"
            amount: Scroll amount in pixels
        """
        scroll_amount = amount if direction == "down" else -amount
        self.execute_script(f"window.scrollBy(0, {scroll_amount});")
        logger.debug(f"Scrolled page {direction} by {amount}px")

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url

    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
        logger.debug("Page refreshed")

    def go_back(self):
        """Navigate back in browser history."""
        self.driver.back()
        logger.debug("Navigated back")

    def take_screenshot(self, filename: str = "screenshot.png") -> bool:
        """
        Take a screenshot of the current page.

        Args:
            filename: Path to save screenshot

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            return False
