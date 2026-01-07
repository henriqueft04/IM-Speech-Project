"""
Google Maps Search Results Page object.
Handles search result selection and extraction.
"""

import logging
from typing import List
from selenium.webdriver.common.by import By

from infrastructure.page_objects.base_page import BasePage
from infrastructure.selenium_helpers import retry_on_stale_element
from domain import Location, SearchResult

logger = logging.getLogger(__name__)


class MapsSearchResultsPage(BasePage):
    """
    Page Object for Google Maps search results.

    Handles:
    - Extracting search results
    - Selecting specific results
    - Getting result details
    """

    # Locators
    SEARCH_RESULTS_CONTAINER = (By.XPATH, "//div[@role='feed' or contains(@class, 'section-layout')]")
    RESULT_ITEMS = (By.XPATH, "//div[@role='feed']//a[contains(@class, 'hfpxzc')]")
    RESULT_TITLES = (By.XPATH, "//div[@role='feed']//div[@class='fontHeadlineSmall']")
    RESULT_LINK = (By.XPATH, ".//a[contains(@class, 'hfpxzc')]")

    # Alternative selectors for different result types
    ALT_RESULT_ITEMS = (By.XPATH, "//div[@role='article']")
    ALT_RESULT_TITLES = (By.XPATH, "//div[@aria-label]//div[contains(@class, 'fontBodyMedium')]")

    def wait_for_results(self, timeout: int = 10) -> bool:
        """
        Wait for search results to load.

        Args:
            timeout: Maximum wait time

        Returns:
            True if results loaded
        """
        try:
            self.find_element(self.SEARCH_RESULTS_CONTAINER, timeout=timeout)
            logger.info("Search results loaded")
            return True
        except Exception as e:
            logger.warning(f"Search results did not load: {e}")
            return False

    @retry_on_stale_element()
    def get_search_results(self, max_results: int = 5) -> List[Location]:
        """
        Extract search results from the page.

        Args:
            max_results: Maximum number of results to extract

        Returns:
            List of Location objects
        """
        locations = []

        try:
            # Wait for results
            if not self.wait_for_results():
                return locations

            # Try primary result selector
            result_elements = self.find_elements(self.RESULT_ITEMS, timeout=5)

            if not result_elements:
                # Try alternative selector
                logger.info("Trying alternative result selector")
                result_elements = self.find_elements(self.ALT_RESULT_ITEMS, timeout=5)

            if not result_elements:
                logger.warning("No search results found")
                return locations

            # Extract location info from each result
            for idx, element in enumerate(result_elements[:max_results]):
                try:
                    # Get title/name
                    name = element.get_attribute("aria-label")
                    if not name:
                        # Try getting text content
                        name = element.text.split('\n')[0] if element.text else f"Result {idx + 1}"

                    # Get href for place ID if available
                    place_id = None
                    try:
                        href = element.get_attribute("href")
                        if href and "/place/" in href:
                            # Extract place ID or coordinates from URL
                            place_id = href.split("/place/")[1].split("/")[0]
                    except:
                        pass

                    location = Location(
                        name=name.strip(),
                        place_id=place_id,
                        metadata={"result_index": idx}
                    )
                    locations.append(location)
                    logger.debug(f"Extracted result {idx + 1}: {location.name}")

                except Exception as e:
                    logger.warning(f"Failed to extract result {idx}: {e}")
                    continue

            logger.info(f"Extracted {len(locations)} search results")
            return locations

        except Exception as e:
            logger.error(f"Failed to get search results: {e}")
            return locations

    def select_result_by_index(self, index: int) -> bool:
        """
        Click on a search result by its index.

        Args:
            index: 0-based index of the result

        Returns:
            True if successful
        """
        try:
            result_elements = self.find_elements(self.RESULT_ITEMS, timeout=5)

            if not result_elements:
                result_elements = self.find_elements(self.ALT_RESULT_ITEMS, timeout=5)

            if index < 0 or index >= len(result_elements):
                logger.error(f"Invalid result index: {index} (total: {len(result_elements)})")
                return False

            # Click the result
            element = result_elements[index]
            self.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.execute_script("arguments[0].click();", element)

            logger.info(f"Selected search result {index + 1}")
            return True

        except Exception as e:
            logger.error(f"Failed to select result {index}: {e}")
            return False

    def select_result_by_name(self, name: str) -> bool:
        """
        Click on a search result by matching name.

        Args:
            name: Name or partial name to match

        Returns:
            True if successful
        """
        try:
            locations = self.get_search_results()

            for idx, location in enumerate(locations):
                if name.lower() in location.name.lower():
                    return self.select_result_by_index(idx)

            logger.warning(f"No result found matching: {name}")
            return False

        except Exception as e:
            logger.error(f"Failed to select result by name '{name}': {e}")
            return False

    def get_top_results(self, n: int = 3) -> SearchResult:
        """
        Get top N search results.

        Args:
            n: Number of results to get

        Returns:
            SearchResult object with locations
        """
        locations = self.get_search_results(max_results=n)

        # Try to extract the search query from page
        query = "Unknown"
        try:
            search_box = self.find_element((By.ID, "searchboxinput"), timeout=2)
            query = search_box.get_attribute("value") or "Unknown"
        except:
            pass

        return SearchResult(
            locations=locations,
            query=query
        )

    def has_results(self) -> bool:
        """
        Check if any search results are present.

        Returns:
            True if results exist
        """
        try:
            result_elements = self.find_elements(self.RESULT_ITEMS, timeout=3)
            if not result_elements:
                result_elements = self.find_elements(self.ALT_RESULT_ITEMS, timeout=3)

            return len(result_elements) > 0

        except Exception:
            return False
