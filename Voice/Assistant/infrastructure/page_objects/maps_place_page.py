"""
Google Maps Place Details Page object.
Handles place information, reviews, and photos.
"""

import logging
from typing import Optional, List, Dict, Any
from selenium.webdriver.common.by import By

from infrastructure.page_objects.base_page import BasePage
from infrastructure.selenium_helpers import retry_on_stale_element
from domain import Location, PlaceDetails

logger = logging.getLogger(__name__)


class MapsPlacePage(BasePage):
    """
    Page Object for Google Maps place details.

    Handles:
    - Extracting place information
    - Viewing reviews
    - Viewing photos
    - Getting opening hours
    """

    # Locators
    PLACE_NAME = (By.XPATH, "//h1[contains(@class, 'fontHeadlineLarge') or @class='fontHeadlineMedium']")
    PLACE_RATING = (By.XPATH, "//div[contains(@aria-label, 'stars') or contains(@aria-label, 'Star rating')]")
    PLACE_RATING_VALUE = (By.XPATH, "//div[@role='img' and contains(@aria-label, 'stars')]")
    TOTAL_RATINGS = (By.XPATH, "//button[contains(@aria-label, 'reviews')]")

    # Address and contact
    ADDRESS = (By.XPATH, "//button[@data-item-id='address']//div[contains(@class, 'fontBodyMedium')]")
    PHONE = (By.XPATH, "//button[@data-item-id='phone:tel:' or contains(@data-item-id, 'phone')]")
    WEBSITE = (By.XPATH, "//a[@data-item-id='authority' or contains(@data-item-id, 'website')]")

    # Opening hours
    HOURS_BUTTON = (By.XPATH, "//button[@data-item-id='oh' or contains(@aria-label, 'Hours')]")
    OPEN_NOW_STATUS = (By.XPATH, "//div[contains(@class, 'fontBodyMedium') and (contains(text(), 'Open') or contains(text(), 'Closed'))]")

    # Tabs
    OVERVIEW_TAB = (By.XPATH, "//button[@role='tab' and contains(@aria-label, 'Overview')]")
    REVIEWS_TAB = (By.XPATH, "//button[@role='tab' and contains(@aria-label, 'Reviews')]")
    PHOTOS_TAB = (By.XPATH, "//button[@role='tab' and contains(@aria-label, 'Photos')]")
    ABOUT_TAB = (By.XPATH, "//button[@role='tab' and contains(@aria-label, 'About')]")

    # Reviews
    REVIEW_ITEMS = (By.XPATH, "//div[@data-review-id or contains(@class, 'review-item')]")
    REVIEW_TEXT = (By.XPATH, ".//span[@class='wiI7pd']")
    REVIEW_RATING = (By.XPATH, ".//span[@aria-label and contains(@aria-label, 'stars')]")

    # Photos
    PHOTO_ITEMS = (By.XPATH, "//button[contains(@aria-label, 'Photo')]//img")
    PHOTO_GRID = (By.XPATH, "//div[contains(@class, 'photo-grid') or contains(@role, 'img')]")

    # Directions button (when on place page)
    DIRECTIONS_BUTTON = (By.XPATH, "//button[@data-value='Directions' or contains(@aria-label, 'Directions')]")

    def wait_for_place_details(self, timeout: int = 10) -> bool:
        """
        Wait for place details to load.

        Args:
            timeout: Maximum wait time

        Returns:
            True if details loaded
        """
        try:
            self.find_element(self.PLACE_NAME, timeout=timeout)
            logger.info("Place details loaded")
            return True
        except Exception as e:
            logger.warning(f"Place details did not load: {e}")
            return False

    @retry_on_stale_element()
    def get_place_name(self) -> Optional[str]:
        """
        Get the place name.

        Returns:
            Place name or None
        """
        try:
            return self.get_text(self.PLACE_NAME)
        except Exception as e:
            logger.error(f"Failed to get place name: {e}")
            return None

    @retry_on_stale_element()
    def get_rating(self) -> Optional[float]:
        """
        Get the place rating.

        Returns:
            Rating value (0-5) or None
        """
        try:
            rating_element = self.find_element(self.PLACE_RATING_VALUE, timeout=5)
            aria_label = rating_element.get_attribute("aria-label")

            if aria_label:
                # Extract number from "X.X stars" or "X stars"
                parts = aria_label.split()
                for part in parts:
                    try:
                        return float(part.replace(',', '.'))
                    except ValueError:
                        continue

            return None

        except Exception as e:
            logger.warning(f"Failed to get rating: {e}")
            return None

    @retry_on_stale_element()
    def get_total_ratings(self) -> Optional[int]:
        """
        Get total number of ratings.

        Returns:
            Number of ratings or None
        """
        try:
            ratings_button = self.find_element(self.TOTAL_RATINGS, timeout=5)
            aria_label = ratings_button.get_attribute("aria-label")

            if aria_label:
                # Extract number from "X reviews" or "X,XXX reviews"
                parts = aria_label.split()
                for part in parts:
                    try:
                        # Remove commas and convert to int
                        return int(part.replace(',', '').replace('.', ''))
                    except ValueError:
                        continue

            return None

        except Exception as e:
            logger.warning(f"Failed to get total ratings: {e}")
            return None

    @retry_on_stale_element()
    def get_address(self) -> Optional[str]:
        """
        Get the place address.

        Returns:
            Address string or None
        """
        try:
            return self.get_text(self.ADDRESS, timeout=5)
        except Exception as e:
            logger.warning(f"Failed to get address: {e}")
            return None

    @retry_on_stale_element()
    def is_open_now(self) -> Optional[bool]:
        """
        Check if place is currently open.

        Returns:
            True if open, False if closed, None if unknown
        """
        try:
            status_text = self.get_text(self.OPEN_NOW_STATUS, timeout=3)

            if status_text:
                status_lower = status_text.lower()
                if "open" in status_lower:
                    return True
                elif "closed" in status_lower:
                    return False

            return None

        except Exception as e:
            logger.warning(f"Failed to get open status: {e}")
            return None

    def get_place_details(self) -> PlaceDetails:
        """
        Get comprehensive place details.

        Returns:
            PlaceDetails object
        """
        try:
            # Wait for details to load
            self.wait_for_place_details()

            # Extract basic info
            name = self.get_place_name() or "Unknown Place"
            rating = self.get_rating()
            total_ratings = self.get_total_ratings()
            address = self.get_address()
            is_open = self.is_open_now()

            # Create location
            location = Location(
                name=name,
                formatted_address=address
            )

            # Create place details
            details = PlaceDetails(
                location=location,
                rating=rating,
                total_ratings=total_ratings,
                is_open_now=is_open
            )

            logger.info(f"Retrieved details for: {name}")
            return details

        except Exception as e:
            logger.error(f"Failed to get place details: {e}")
            # Return minimal details
            return PlaceDetails(location=Location(name="Unknown Place"))

    def show_reviews(self) -> bool:
        """
        Navigate to reviews tab.

        Returns:
            True if successful
        """
        try:
            self.click(self.REVIEWS_TAB)
            logger.info("Opened reviews tab")
            return True
        except Exception as e:
            logger.error(f"Failed to open reviews: {e}")
            return False

    @retry_on_stale_element()
    def get_reviews(self, max_reviews: int = 5) -> List[Dict[str, Any]]:
        """
        Get place reviews.

        Args:
            max_reviews: Maximum number of reviews to extract

        Returns:
            List of review dictionaries
        """
        reviews = []

        try:
            # Make sure we're on reviews tab
            if not self.is_element_visible(self.REVIEW_ITEMS, timeout=3):
                self.show_reviews()

            # Get review elements
            review_elements = self.find_elements(self.REVIEW_ITEMS, timeout=5)

            for element in review_elements[:max_reviews]:
                try:
                    # Extract review text
                    text = ""
                    try:
                        text_element = element.find_element(*self.REVIEW_TEXT)
                        text = text_element.text
                    except:
                        pass

                    # Extract rating if available
                    rating = None
                    try:
                        rating_element = element.find_element(*self.REVIEW_RATING)
                        aria_label = rating_element.get_attribute("aria-label")
                        if aria_label:
                            rating = float(aria_label.split()[0])
                    except:
                        pass

                    if text or rating:
                        reviews.append({
                            "text": text,
                            "rating": rating
                        })

                except Exception as e:
                    logger.warning(f"Failed to extract review: {e}")
                    continue

            logger.info(f"Extracted {len(reviews)} reviews")
            return reviews

        except Exception as e:
            logger.error(f"Failed to get reviews: {e}")
            return reviews

    def show_photos(self) -> bool:
        """
        Navigate to photos tab.

        Returns:
            True if successful
        """
        try:
            self.click(self.PHOTOS_TAB)
            logger.info("Opened photos tab")
            return True
        except Exception as e:
            logger.error(f"Failed to open photos: {e}")
            return False

    def get_directions_to_place(self) -> bool:
        """
        Click directions button from place page.

        Returns:
            True if successful
        """
        try:
            self.click(self.DIRECTIONS_BUTTON)
            logger.info("Clicked directions button")
            return True
        except Exception as e:
            logger.error(f"Failed to click directions: {e}")
            return False
