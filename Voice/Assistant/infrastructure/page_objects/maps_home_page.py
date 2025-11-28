"""
Google Maps Home Page object.
Handles search, map controls, and navigation.
"""

import logging
import time
from typing import Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from infrastructure.page_objects.base_page import BasePage
from infrastructure.selenium_helpers import retry_on_stale_element
from domain import Location, SearchResult, MapType, ZoomLevel

logger = logging.getLogger(__name__)


class MapsHomePage(BasePage):
    """
    Page Object for Google Maps home page.

    Handles:
    - Search functionality
    - Map type switching
    - Zoom controls
    - Traffic layer
    """

    # Locators
    SEARCH_BOX = (By.XPATH, "//input[@id='searchboxinput' or @aria-label='Search Google Maps' or @aria-label='Pesquisar no Google Maps' or contains(@placeholder, 'Search') or contains(@placeholder, 'Pesquisar')]")
    SEARCH_BUTTON = (By.XPATH, "//button[@id='searchbox-searchbutton' or @aria-label='Search' or @aria-label='Pesquisar']")

    # Map controls
    ZOOM_IN_BUTTON = (By.XPATH, "//button[@aria-label='Aumentar' or @aria-label='Zoom in']")
    ZOOM_OUT_BUTTON = (By.XPATH, "//button[@aria-label='Diminuir' or @aria-label='Zoom out']")

    # Map controls - New UI
    # MINIMAP = (By.ID, "minimap") # Removed as it no longer exists
    # SHOW_IMAGES_BUTTON = (By.XPATH, "//button[@aria-label='Mostrar imagens' or @aria-label='Show imagery' or @aria-label='Explorar' or @aria-label='Explore']")
    LAYERS_MENU_BUTTON = (By.XPATH, "//button[contains(@aria-label, 'Camadas') or contains(@aria-label, 'Layers') or @class='yHc72 qk5Wte']")
    MORE_BUTTON = (By.XPATH, "//button[.//label[text()='Mais'] or .//label[text()='More']]")

    # Map details modal
    MAP_DETAILS_MODAL = (By.XPATH, "//h2[contains(text(), 'Detalhes do mapa') or contains(text(), 'Map details')]")

    # Map type options in modal (Tipo de mapa section)
    SATELLITE_BUTTON = (By.XPATH, "//button[.//label[text()='Satélite'] or .//label[text()='Satellite']]")
    TERRAIN_BUTTON = (By.XPATH, "//button[.//label[text()='Relevo'] or .//label[text()='Terrain']]")
    TRAFFIC_BUTTON = (By.XPATH, "//button[.//label[text()='Trânsito'] or .//label[text()='Traffic']]")
    BICYCLE_BUTTON = (By.XPATH, "//button[.//label[text()='De bicicleta'] or .//label[text()='Bicycling']]")
    DEFAULT_MAP_BUTTON = (By.XPATH, "//button[.//label[text()='Predefinição'] or .//label[text()='Default']]")

    # My location
    MY_LOCATION_BUTTON = (By.XPATH, "//button[@aria-label='Your location' or @aria-label='Show Your Location']")

    # Directions (supports English and Portuguese)
    DIRECTIONS_BUTTON = (By.XPATH, "//button[@aria-label='Directions' or @aria-label='Direções' or @data-value='Directions']")
    DIRECTIONS_ORIGIN_INPUT = (By.XPATH, "//input[contains(@aria-label, 'starting point') or contains(@aria-label, 'ponto de partida') or contains(@placeholder, 'origem')]")
    DIRECTIONS_DEST_INPUT = (By.XPATH, "//input[contains(@aria-label, 'destination') or contains(@aria-label, 'destino') or contains(@placeholder, 'destino')]")

    # Transport mode buttons (in directions panel)
    DRIVING_MODE = (By.XPATH, "//button[@data-tooltip='Carro' or @data-tooltip='Driving' or .//div[@aria-label='Carro' or @aria-label='Driving']]")
    TRANSIT_MODE = (By.XPATH, "//button[@data-tooltip='Transportes públicos' or @data-tooltip='Transit' or .//div[contains(@aria-label, 'Transportes') or @aria-label='Transit']]")
    WALKING_MODE = (By.XPATH, "//button[@data-tooltip='Caminhar' or @data-tooltip='A pé' or @data-tooltip='Walking' or .//div[@aria-label='Caminhar' or @aria-label='A pé' or @aria-label='Walking']]")
    CYCLING_MODE = (By.XPATH, "//button[@data-tooltip='Bicicleta' or @data-tooltip='Cycling' or .//div[contains(@aria-label, 'Bicicleta') or @aria-label='Cycling']]")

    # Navigation
    START_NAVIGATION_BUTTON = (By.XPATH, "//button[contains(@aria-label, 'Start') or contains(., 'Start')]")



    def search(self, query: str) -> bool:
        """
        Search for a location.

        Args:
            query: Search query (place name, address, etc.)

        Returns:
            True if search initiated successfully
        """
        try:
            logger.info(f"Searching for: {query}")

            # Click and clear search box
            self.click(self.SEARCH_BOX)
            self.send_keys(self.SEARCH_BOX, query, clear_first=True)

            # Press Enter or click search button
            search_box = self.find_element(self.SEARCH_BOX)
            search_box.send_keys(Keys.RETURN)

            logger.info(f"Search initiated for: {query}")
            return True

        except Exception as e:
            logger.error(f"Failed to search for '{query}': {e}")
            return False

    def zoom_in(self, clicks: int = 1):
        """
        Zoom in on the map.

        Args:
            clicks: Number of zoom clicks
        """
        try:
            for _ in range(clicks):
                self.click(self.ZOOM_IN_BUTTON)
            logger.info(f"Zoomed in {clicks} level(s)")
        except Exception as e:
            logger.error(f"Failed to zoom in: {e}")
            # Fallback: keyboard shortcut
            self.send_keyboard_shortcut(Keys.ADD)  # '+' key

    def zoom_out(self, clicks: int = 1):
        """
        Zoom out on the map.

        Args:
            clicks: Number of zoom clicks
        """
        try:
            for _ in range(clicks):
                self.click(self.ZOOM_OUT_BUTTON)
            logger.info(f"Zoomed out {clicks} level(s)")
        except Exception as e:
            logger.error(f"Failed to zoom out: {e}")
            # Fallback: keyboard shortcut
            self.send_keyboard_shortcut(Keys.SUBTRACT)  # '-' key

    def set_zoom_level(self, zoom_level: ZoomLevel):
        """
        Set zoom level based on ZoomLevel enum.

        Args:
            zoom_level: Zoom intensity
        """
        clicks = zoom_level.value
        return clicks

    def open_map_details_modal(self) -> bool:
        """
        Open the map details modal by hovering 'Camadas' and clicking 'Mais'.

        Returns:
            True if modal opened successfully
        """
        try:
            # 1. Hover over 'Camadas' button
            layers_btn = self.find_element(self.LAYERS_MENU_BUTTON, timeout=5)
            actions = ActionChains(self.driver)
            actions.move_to_element(layers_btn).perform()
            logger.info("Hovered over 'Camadas' button")

            # Wait a moment for the menu to expand
            time.sleep(1.0)

            # 2. Click "Mais" button
            self.click(self.MORE_BUTTON, timeout=5)
            logger.info("Clicked 'Mais' button")

            # Wait for modal to appear
            self.find_element(self.MAP_DETAILS_MODAL, timeout=5)
            logger.info("Map details modal opened")
            return True

        except Exception as e:
            logger.error(f"Failed to open map details modal: {e}")
            return False

    def close_map_details_modal(self) -> bool:
        """
        Close the map details modal.

        Returns:
            True if successful
        """
        try:
            # Press Escape to close modal
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ESCAPE).perform()
            logger.info("Closed map details modal")
            return True
        except Exception as e:
            logger.error(f"Failed to close modal: {e}")
            return False

    def reset_map_state(self) -> bool:
        """
        Reset Google Maps to clean state by closing all panels.
        Tries to click close buttons for directions panel and other sidebars.

        Returns:
            True if successful
        """
        try:
            # Try to find and click the close button for directions/search panel
            close_button_xpaths = [
                "//button[@aria-label='Close directions' or @aria-label='Fechar direções']",
                "//button[contains(@aria-label, 'Close') or contains(@aria-label, 'Fechar')]",
                "//button[@aria-label='Clear search' or @aria-label='Limpar pesquisa']",
                "//div[@id='pane']//button[contains(@aria-label, 'Close')]",
                "//aside//button[contains(@aria-label, 'Close')]",
            ]

            closed_something = False
            for xpath in close_button_xpaths:
                try:
                    close_button = self.driver.find_element(By.XPATH, xpath)
                    if close_button.is_displayed():
                        close_button.click()
                        logger.info(f"Clicked close button: {xpath}")
                        closed_something = True
                        time.sleep(0.5)  # Wait for animation
                        break  # Stop after first successful close
                except:
                    continue

            # Also press ESC a couple times as backup
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ESCAPE).perform()
            time.sleep(0.2)
            actions.send_keys(Keys.ESCAPE).perform()

            logger.info(f"Reset map state - {'closed panel' if closed_something else 'pressed ESC'}")
            return True
        except Exception as e:
            logger.error(f"Failed to reset map state: {e}")
            return False

    def toggle_traffic_layer(self, show: bool) -> bool:
        """
        Toggle traffic layer on/off.

        Args:
            show: True to show traffic, False to hide

        Returns:
            True if successful
        """
        try:
            # Traffic layer button XPaths
            traffic_button_xpaths = [
                "//button[@aria-label='Show traffic' or @aria-label='Mostrar trânsito']",
                "//button[@aria-label='Hide traffic' or @aria-label='Esconder trânsito']",
                "//button[contains(@aria-label, 'traffic') or contains(@aria-label, 'trânsito')]",
                "//button[@data-value='Traffic']",
            ]

            # Try to find traffic toggle button
            traffic_button = None
            for xpath in traffic_button_xpaths:
                try:
                    btn = self.driver.find_element(By.XPATH, xpath)
                    if btn.is_displayed():
                        traffic_button = btn
                        break
                except:
                    continue

            if not traffic_button:
                logger.warning("Traffic toggle button not found")
                return False

            # Check current state from aria-label
            current_label = traffic_button.get_attribute("aria-label") or ""
            is_currently_shown = "hide" in current_label.lower() or "esconder" in current_label.lower()

            # Click if we need to change state
            if (show and not is_currently_shown) or (not show and is_currently_shown):
                traffic_button.click()
                time.sleep(0.5)  # Wait for layer to toggle
                logger.info(f"Toggled traffic layer: show={show}")

            return True

        except Exception as e:
            logger.error(f"Failed to toggle traffic layer: {e}")
            return False

    def change_map_type(self, map_type: MapType) -> bool:
        """
        Change the map view type using the new UI.

        Args:
            map_type: Desired map type

        Returns:
            True if successful
        """
        try:
            # Open the map details modal
            if not self.open_map_details_modal():
                return False

            # Select map type from "Tipo de mapa" section
            if map_type == MapType.SATELLITE:
                self.click(self.SATELLITE_BUTTON, timeout=5)
            elif map_type == MapType.TERRAIN:
                self.click(self.TERRAIN_BUTTON, timeout=5)
            elif map_type == MapType.TRAFFIC:
                self.click(self.TRAFFIC_BUTTON, timeout=5)
            else:  # DEFAULT
                self.click(self.DEFAULT_MAP_BUTTON, timeout=5)

            logger.info(f"Changed map type to: {map_type.value}")

            # Close modal
            self.close_map_details_modal()

            return True

        except Exception as e:
            logger.error(f"Failed to change map type to {map_type.value}: {e}")
            # Try to close modal on error
            try:
                self.close_map_details_modal()
            except:
                pass

            return False

    def recenter_map(self) -> bool:
        """
        Recenter map to current location.

        Returns:
            True if successful
        """
        try:
            self.click(self.MY_LOCATION_BUTTON)
            logger.info("Recentered map to current location")
            return True
        except Exception as e:
            logger.error(f"Failed to recenter map: {e}")
            return False

    def open_directions(self) -> bool:
        """
        Open the directions panel.

        Returns:
            True if successful
        """
        try:
            self.click(self.DIRECTIONS_BUTTON)
            logger.info("Opened directions panel")
            return True
        except Exception as e:
            logger.error(f"Failed to open directions: {e}")
            return False

    def set_directions(
        self,
        destination: str,
        origin: Optional[str] = None
    ) -> bool:
        """
        Set origin and destination for directions.

        Args:
            destination: Destination location
            origin: Origin location (optional, uses current location if None)

        Returns:
            True if successful
        """
        try:
            wait = WebDriverWait(self.driver, 10)

            # Open directions if not already open
            if not self.is_element_visible(self.DIRECTIONS_DEST_INPUT, timeout=5):
                self.open_directions()
                # Wait for destination input to be clickable
                wait.until(EC.element_to_be_clickable(self.DIRECTIONS_DEST_INPUT))

            # Set origin if provided
            if origin:
                origin_input = wait.until(EC.element_to_be_clickable(self.DIRECTIONS_ORIGIN_INPUT))
                origin_input.clear()
                origin_input.send_keys(origin)
                origin_input.send_keys(Keys.RETURN)

            # Set destination
            dest_input = wait.until(EC.element_to_be_clickable(self.DIRECTIONS_DEST_INPUT))
            dest_input.clear()
            dest_input.send_keys(destination)
            dest_input.send_keys(Keys.RETURN)

            logger.info(f"Set directions: {origin or 'Current location'} -> {destination}")
            return True

        except Exception as e:
            logger.error(f"Failed to set directions: {e}")
            return False

    def select_transport_mode(self, mode_button_locator: tuple) -> bool:
        """
        Select a transport mode.

        Args:
            mode_button_locator: Locator for the mode button

        Returns:
            True if successful
        """
        try:
            self.click(mode_button_locator)
            return True
        except Exception as e:
            logger.error(f"Failed to select transport mode: {e}")
            return False

    def start_navigation(self) -> bool:
        """
        Start turn-by-turn navigation.

        Returns:
            True if successful
        """
        try:
            self.click(self.START_NAVIGATION_BUTTON)
            logger.info("Started navigation")
            return True
        except Exception as e:
            logger.error(f"Failed to start navigation: {e}")
            return False
