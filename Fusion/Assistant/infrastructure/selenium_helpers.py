"""
Selenium utility functions and decorators.
Provides retry logic, smart waits, and error handling.
"""

import logging
import time
from functools import wraps
from typing import Callable, Tuple, Any

from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import MAX_RETRY_ATTEMPTS, SELENIUM_TIMEOUT

logger = logging.getLogger(__name__)


class SeleniumException(Exception):
    """Base exception for selenium operations."""
    pass


class ElementNotFoundException(SeleniumException):
    """Element could not be found."""
    pass


class ElementNotClickableException(SeleniumException):
    """Element is not clickable."""
    pass


def retry_on_stale_element(max_attempts: int = MAX_RETRY_ATTEMPTS):
    """
    Decorator to retry operations that fail due to stale element references.

    Args:
        max_attempts: Maximum number of retry attempts
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except StaleElementReferenceException as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Stale element in {func.__name__}, "
                            f"attempt {attempt + 1}/{max_attempts}"
                        )
                        time.sleep(0.5)
                    else:
                        logger.error(f"Max retries exceeded in {func.__name__}")

            raise last_exception

        return wrapper
    return decorator


def retry_on_click_intercepted(max_attempts: int = MAX_RETRY_ATTEMPTS):
    """
    Decorator to retry click operations that are intercepted.

    Args:
        max_attempts: Maximum number of retry attempts
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (ElementClickInterceptedException, ElementNotInteractableException) as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Click intercepted in {func.__name__}, "
                            f"attempt {attempt + 1}/{max_attempts}"
                        )
                        time.sleep(0.5)
                    else:
                        logger.error(f"Max retries exceeded in {func.__name__}")

            raise ElementNotClickableException(
                f"Element not clickable after {max_attempts} attempts"
            ) from last_exception

        return wrapper
    return decorator


def safe_click(element: WebElement, driver: WebDriver = None) -> bool:
    """
    Safely click an element with fallback strategies.

    Args:
        element: WebElement to click
        driver: WebDriver instance (optional, for JS click fallback)

    Returns:
        True if click succeeded, False otherwise
    """
    try:
        # Try normal click first
        element.click()
        return True
    except (ElementClickInterceptedException, ElementNotInteractableException):
        if driver:
            try:
                # Fallback to JavaScript click
                logger.info("Falling back to JavaScript click")
                driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as e:
                logger.error(f"JavaScript click failed: {e}")
                return False
        return False


def wait_for_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    timeout: int = SELENIUM_TIMEOUT,
    condition: Callable = EC.visibility_of_element_located
) -> WebElement:
    """
    Wait for an element with a specific condition.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By.TYPE, "locator_value")
        timeout: Maximum wait time in seconds
        condition: Expected condition to wait for

    Returns:
        WebElement when condition is met

    Raises:
        ElementNotFoundException: If element not found within timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(condition(locator))
        return element
    except TimeoutException:
        raise ElementNotFoundException(
            f"Element {locator} not found within {timeout}s"
        )


def wait_for_element_clickable(
    driver: WebDriver,
    locator: Tuple[str, str],
    timeout: int = SELENIUM_TIMEOUT
) -> WebElement:
    """
    Wait for an element to be clickable.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By.TYPE, "locator_value")
        timeout: Maximum wait time in seconds

    Returns:
        Clickable WebElement
    """
    return wait_for_element(
        driver,
        locator,
        timeout,
        EC.element_to_be_clickable
    )


def wait_for_elements(
    driver: WebDriver,
    locator: Tuple[str, str],
    timeout: int = SELENIUM_TIMEOUT
) -> list:
    """
    Wait for multiple elements to be present.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By.TYPE, "locator_value")
        timeout: Maximum wait time in seconds

    Returns:
        List of WebElements
    """
    try:
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
        return elements
    except TimeoutException:
        return []


def is_element_present(
    driver: WebDriver,
    locator: Tuple[str, str],
    timeout: int = 2
) -> bool:
    """
    Check if an element is present without raising exceptions.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By.TYPE, "locator_value")
        timeout: Maximum wait time in seconds

    Returns:
        True if element is present, False otherwise
    """
    try:
        wait_for_element(driver, locator, timeout, EC.presence_of_element_located)
        return True
    except ElementNotFoundException:
        return False


def scroll_to_element(driver: WebDriver, element: WebElement):
    """
    Scroll element into view.

    Args:
        driver: WebDriver instance
        element: WebElement to scroll to
    """
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
        element
    )
    time.sleep(0.3)  # Small delay for smooth scroll


def take_screenshot_on_failure(filename: str = "failure_screenshot.png"):
    """
    Decorator to take screenshot on function failure.

    Args:
        filename: Name of the screenshot file
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if hasattr(self, 'driver'):
                    try:
                        self.driver.save_screenshot(filename)
                        logger.info(f"Screenshot saved: {filename}")
                    except Exception as screenshot_error:
                        logger.error(f"Failed to save screenshot: {screenshot_error}")
                raise e

        return wrapper
    return decorator
