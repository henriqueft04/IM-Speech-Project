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
    SEARCH_BOX = (By.ID, "searchboxinput")
    SEARCH_BUTTON = (By.ID, "searchbox-searchbutton")

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
    DRIVING_MODE = (By.XPATH, "//button[@aria-label='Driving' or @data-value='Driving']")
    TRANSIT_MODE = (By.XPATH, "//button[@aria-label='Transit' or @data-value='Transit']")
    WALKING_MODE = (By.XPATH, "//button[@aria-label='Walking' or @data-value='Walking']")
    CYCLING_MODE = (By.XPATH, "//button[@aria-label='Cycling' or @data-value='Cycling']")

    # Navigation
    START_NAVIGATION_BUTTON = (By.XPATH, "//button[contains(@aria-label, 'Start') or contains(., 'Start')]")

    # Street View and Explore
    PEGMAN_BUTTON = (By.XPATH, "//button[contains(@aria-label, 'Pegman') or contains(@aria-label, 'Street View') or contains(@class, 'widget-minimap-pegman')]")
    STREET_VIEW_EXIT = (By.XPATH, "//button[contains(@aria-label, 'Voltar') or contains(@aria-label, 'Back') or contains(@aria-label, 'Fechar') or contains(@aria-label, 'Close') or contains(@jsaction, 'pane.close')]")
    EXPLORE_BUTTON = (By.XPATH, "//button[contains(@aria-label, 'Explorar') or contains(@aria-label, 'Explore') or contains(., 'Coisas a fazer') or contains(., 'Things to do') or @aria-label='Mostrar imagens' or @aria-label='Show imagery' or contains(@aria-label, 'Atividades') or contains(@aria-label, 'Activities')]")

    # Map canvas for interactions
    MAP_CANVAS = (By.CSS_SELECTOR, "canvas.widget-scene-canvas")

    # Street View specific elements
    STREET_VIEW_CONTAINER = (By.XPATH, "//div[contains(@class, 'widget-scene')]//canvas | //div[@id='street-view']")
    STREET_VIEW_ADDRESS_BOX = (By.XPATH, "//div[contains(@class, 'widget-titlecard')]")
    MINIMAP = (By.XPATH, "//div[contains(@class, 'widget-minimap')] | //div[@id='minimap']")

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

    def zoom_out(self, clicks: int = 1):
        """
        Zoom out on the map.

        Args:
            clicks: Number of zoom clicks
        """
        try:
            # Method 1: Try clicking the zoom out button
            zoom_out_selectors = [
                self.ZOOM_OUT_BUTTON,
                (By.XPATH, "//button[@aria-label='Diminuir' or @aria-label='Zoom out']"),
                (By.XPATH, "//button[contains(@aria-label, 'Diminuir') or contains(@aria-label, 'Zoom out')]"),
                (By.XPATH, "//button[@id='widget-zoom-out']"),
                (By.CSS_SELECTOR, "button[aria-label*='Zoom out'], button[aria-label*='Diminuir']"),
            ]

            button_found = False
            for selector in zoom_out_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed():
                        for _ in range(clicks):
                            element.click()
                            time.sleep(0.3)
                        logger.info(f"Zoomed out {clicks} level(s) via button")
                        button_found = True
                        break
                except Exception:
                    continue

            if button_found:
                return

            # Method 2: Try keyboard shortcuts
            # First focus on the map
            try:
                map_element = self.driver.find_element(By.CSS_SELECTOR, "canvas.widget-scene-canvas")
                map_element.click()
            except Exception:
                try:
                    self.driver.find_element(By.TAG_NAME, "body").click()
                except Exception:
                    pass

            time.sleep(0.2)

            # Try minus key
            actions = ActionChains(self.driver)
            for _ in range(clicks):
                actions.send_keys("-")  # Minus key
            actions.perform()
            logger.info(f"Zoomed out {clicks} level(s) via keyboard (-)")

        except Exception as e:
            logger.error(f"Failed to zoom out: {e}")
            # Last fallback: try PyAutoGUI scroll
            try:
                if PYAUTOGUI_AVAILABLE:
                    # Get window center
                    window_rect = self.driver.get_window_rect()
                    center_x = window_rect['x'] + window_rect['width'] // 2
                    center_y = window_rect['y'] + window_rect['height'] // 2 + 50

                    pyautogui.moveTo(center_x, center_y, duration=0.1)
                    for _ in range(clicks):
                        pyautogui.scroll(-3)  # Negative = zoom out
                        time.sleep(0.2)
                    logger.info(f"Zoomed out {clicks} level(s) via scroll")
            except Exception as scroll_error:
                logger.error(f"Scroll fallback also failed: {scroll_error}")

    def zoom_in(self, clicks: int = 1):
        """
        Zoom in on the map.

        Args:
            clicks: Number of zoom clicks
        """
        try:
            # Method 1: Try clicking the zoom in button
            zoom_in_selectors = [
                self.ZOOM_IN_BUTTON,
                (By.XPATH, "//button[@aria-label='Aumentar' or @aria-label='Zoom in']"),
                (By.XPATH, "//button[contains(@aria-label, 'Aumentar') or contains(@aria-label, 'Zoom in')]"),
                (By.XPATH, "//button[@id='widget-zoom-in']"),
                (By.CSS_SELECTOR, "button[aria-label*='Zoom in'], button[aria-label*='Aumentar']"),
            ]

            button_found = False
            for selector in zoom_in_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed():
                        for _ in range(clicks):
                            element.click()
                            time.sleep(0.3)
                        logger.info(f"Zoomed in {clicks} level(s) via button")
                        button_found = True
                        break
                except Exception:
                    continue

            if button_found:
                return

            # Method 2: Try keyboard shortcuts
            # First focus on the map
            try:
                map_element = self.driver.find_element(By.CSS_SELECTOR, "canvas.widget-scene-canvas")
                map_element.click()
            except Exception:
                try:
                    self.driver.find_element(By.TAG_NAME, "body").click()
                except Exception:
                    pass

            time.sleep(0.2)

            # Try plus key
            actions = ActionChains(self.driver)
            for _ in range(clicks):
                actions.send_keys("+")  # Plus key
            actions.perform()
            logger.info(f"Zoomed in {clicks} level(s) via keyboard (+)")

        except Exception as e:
            logger.error(f"Failed to zoom in: {e}")
            # Last fallback: try PyAutoGUI scroll
            try:
                if PYAUTOGUI_AVAILABLE:
                    # Get window center
                    window_rect = self.driver.get_window_rect()
                    center_x = window_rect['x'] + window_rect['width'] // 2
                    center_y = window_rect['y'] + window_rect['height'] // 2 + 50

                    pyautogui.moveTo(center_x, center_y, duration=0.1)
                    for _ in range(clicks):
                        pyautogui.scroll(3)  # Positive = zoom in
                        time.sleep(0.2)
                    logger.info(f"Zoomed in {clicks} level(s) via scroll")
            except Exception as scroll_error:
                logger.error(f"Scroll fallback also failed: {scroll_error}")

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

    def click_filter_button(self, filter_name: str) -> bool:
        """
        Click on a filter button (e.g., Restaurantes, Hotéis, Postos de combustível).

        Args:
            filter_name: Name of the filter to click

        Returns:
            True if successful
        """
        try:
            # Google Maps filter buttons are typically in a horizontal scroll area
            # They can be identified by their text or aria-label
            filter_locator = (By.XPATH, f"//button[contains(., '{filter_name}') or contains(@aria-label, '{filter_name}')]")

            self.click(filter_locator)
            logger.info(f"Clicked filter button: {filter_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to click filter button '{filter_name}': {e}")
            return False

    def pan_map(self, direction: str, times: int = 3) -> bool:
        """
        Pan the map in a direction using keyboard arrow keys.
        This is more reliable than drag-and-drop for Google Maps.

        Args:
            direction: Direction to pan ('left', 'right', 'up', 'down')
            times: Number of times to press the arrow key (default 3)

        Returns:
            True if successful
        """
        try:
            # Map directions to arrow keys
            direction_keys = {
                "left": Keys.ARROW_LEFT,
                "right": Keys.ARROW_RIGHT,
                "up": Keys.ARROW_UP,
                "down": Keys.ARROW_DOWN
            }

            key = direction_keys.get(direction.lower())
            if not key:
                logger.error(f"Invalid direction: {direction}")
                return False

            # Click on the map area first to focus it
            # Use the canvas element or body as fallback
            try:
                # Try to find and click on the map canvas
                map_element = self.driver.find_element(By.CSS_SELECTOR, "canvas.widget-scene-canvas")
                map_element.click()
            except Exception:
                try:
                    # Fallback: click on the main content area
                    map_element = self.driver.find_element(By.ID, "scene")
                    map_element.click()
                except Exception:
                    # Last fallback: just use body
                    body = self.driver.find_element(By.TAG_NAME, "body")
                    body.click()

            # Use ActionChains to send arrow keys
            actions = ActionChains(self.driver)
            for _ in range(times):
                actions.send_keys(key)
            actions.perform()

            logger.info(f"Panned map {direction} ({times} times)")
            return True

        except Exception as e:
            logger.error(f"Failed to pan map {direction}: {e}")
            return False

    def _pan_map_js(self, direction: str, times: int = 3) -> bool:
        """
        Pan the map using JavaScript execution.

        Args:
            direction: Direction to pan
            times: Number of operations

        Returns:
            True if successful
        """
        try:
            # Calculate pixel offset based on direction
            # Larger values = more noticeable movement
            pixel_offset = 200

            direction_map = {
                "left": (pixel_offset, 0),      # Move map content left (view goes right)
                "right": (-pixel_offset, 0),    # Move map content right (view goes left)
                "up": (0, pixel_offset),        # Move map content up (view goes down)
                "down": (0, -pixel_offset)      # Move map content down (view goes up)
            }

            offset = direction_map.get(direction.lower())
            if not offset:
                return False

            # Find the map canvas
            canvas_selectors = [
                "canvas.widget-scene-canvas",
                "#scene canvas",
                ".widget-scene canvas",
                "canvas",
            ]

            canvas = None
            for selector in canvas_selectors:
                try:
                    canvas = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if canvas.is_displayed():
                        break
                except Exception:
                    continue

            if not canvas:
                logger.debug("Could not find map canvas for JS panning")
                return False

            # Get canvas position and size
            rect = canvas.rect
            center_x = rect['x'] + rect['width'] // 2
            center_y = rect['y'] + rect['height'] // 2

            for i in range(times):
                # Simulate mouse drag using JavaScript events
                js_script = """
                    var canvas = arguments[0];
                    var startX = arguments[1];
                    var startY = arguments[2];
                    var endX = arguments[3];
                    var endY = arguments[4];

                    // Create and dispatch mousedown
                    var mousedown = new MouseEvent('mousedown', {
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        clientX: startX,
                        clientY: startY,
                        button: 0
                    });
                    canvas.dispatchEvent(mousedown);

                    // Create and dispatch mousemove
                    var mousemove = new MouseEvent('mousemove', {
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        clientX: endX,
                        clientY: endY,
                        button: 0
                    });
                    canvas.dispatchEvent(mousemove);

                    // Create and dispatch mouseup
                    var mouseup = new MouseEvent('mouseup', {
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        clientX: endX,
                        clientY: endY,
                        button: 0
                    });
                    canvas.dispatchEvent(mouseup);
                """

                end_x = center_x + offset[0]
                end_y = center_y + offset[1]

                self.driver.execute_script(js_script, canvas, center_x, center_y, end_x, end_y)
                time.sleep(0.3)

            logger.info(f"Panned map {direction} via JS ({times} times)")
            return True

        except Exception as e:
            logger.debug(f"JS pan failed: {e}")
            return False

    def _pan_map_drag(self, direction: str, times: int = 3) -> bool:
        """
        Pan the map using Selenium ActionChains drag.

        Args:
            direction: Direction to pan
            times: Number of operations

        Returns:
            True if successful
        """
        try:
            # Pixel offsets - drag in OPPOSITE direction to pan
            # To see what's on the LEFT, drag the map to the RIGHT
            pixel_offset = 150

            direction_offsets = {
                "left": (pixel_offset, 0),      # Drag right to pan left
                "right": (-pixel_offset, 0),    # Drag left to pan right
                "up": (0, pixel_offset),        # Drag down to pan up
                "down": (0, -pixel_offset)      # Drag up to pan down
            }

            offset = direction_offsets.get(direction.lower())
            if not offset:
                return False

            # Find draggable element
            drag_selectors = [
                (By.CSS_SELECTOR, "canvas.widget-scene-canvas"),
                (By.CSS_SELECTOR, "#scene"),
                (By.CSS_SELECTOR, ".widget-scene"),
                (By.ID, "map"),
                (By.CSS_SELECTOR, "[aria-label='Map']"),
                (By.CSS_SELECTOR, "[aria-label='Mapa']"),
            ]

            drag_element = None
            for selector in drag_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed() and element.size['width'] > 100:
                        drag_element = element
                        logger.debug(f"Found drag element with selector: {selector}")
                        break
                except Exception:
                    continue

            if not drag_element:
                logger.debug("Could not find element to drag")
                return False

            for i in range(times):
                actions = ActionChains(self.driver)

                # Move to center of element first
                actions.move_to_element(drag_element)
                actions.pause(0.1)

                # Click, hold, drag, release
                actions.click_and_hold()
                actions.pause(0.1)
                actions.move_by_offset(offset[0], offset[1])
                actions.pause(0.1)
                actions.release()

                actions.perform()
                time.sleep(0.4)

            logger.info(f"Panned map {direction} via drag ({times} times)")
            return True

        except Exception as e:
            logger.debug(f"Drag pan failed: {e}")
            return False

    def _pan_map_keyboard_focused(self, direction: str, times: int = 3) -> bool:
        """
        Pan the map using keyboard arrows with proper element focus.

        Args:
            direction: Direction to pan
            times: Number of key presses

        Returns:
            True if successful
        """
        try:
            direction_keys = {
                "left": Keys.ARROW_LEFT,
                "right": Keys.ARROW_RIGHT,
                "up": Keys.ARROW_UP,
                "down": Keys.ARROW_DOWN
            }

            key = direction_keys.get(direction.lower())
            if not key:
                return False

            # Find and focus the map element
            focus_selectors = [
                (By.CSS_SELECTOR, "canvas.widget-scene-canvas"),
                (By.CSS_SELECTOR, "#scene"),
                (By.CSS_SELECTOR, ".widget-scene"),
                (By.CSS_SELECTOR, "[role='application']"),
                (By.CSS_SELECTOR, "[aria-label='Map']"),
                (By.CSS_SELECTOR, "[aria-label='Mapa']"),
            ]

            focused = False
            for selector in focus_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed():
                        # Click to focus
                        actions = ActionChains(self.driver)
                        actions.move_to_element(element)
                        actions.click()
                        actions.perform()
                        focused = True
                        logger.debug(f"Focused element with selector: {selector}")
                        time.sleep(0.2)
                        break
                except Exception:
                    continue

            if not focused:
                # Try clicking on body as fallback
                self.driver.find_element(By.TAG_NAME, "body").click()
                time.sleep(0.2)

            # Send arrow keys
            actions = ActionChains(self.driver)
            for _ in range(times):
                actions.send_keys(key)
                actions.pause(0.15)
            actions.perform()

            logger.info(f"Panned map {direction} via keyboard ({times} times)")
            return True

        except Exception as e:
            logger.debug(f"Keyboard pan failed: {e}")
            return False

    def _pan_map_keyboard(self, direction: str, times: int = 3) -> bool:
        """
        Legacy fallback method for keyboard panning.
        """
        return self._pan_map_keyboard_focused(direction, times)

    def enter_street_view(self) -> bool:
        """
        Enter Street View mode using multiple strategies:
        1. Try dragging Pegman onto the map
        2. Try clicking on Street View blue lines
        3. Try keyboard shortcut

        Returns:
            True if successfully entered Street View
        """
        try:
            # First, make sure we're not already in Street View
            if self._is_in_street_view():
                logger.info("Already in Street View mode")
                return True

            # Strategy 1: Try using Pegman drag-and-drop
            if self._enter_street_view_via_pegman():
                return True

            # Strategy 2: Try clicking on Street View layer (blue lines on roads)
            if self._enter_street_view_via_click():
                return True

            # Strategy 3: Try using keyboard shortcut (Ctrl+Shift+G in some versions)
            if self._enter_street_view_via_keyboard():
                return True

            logger.warning("Could not enter Street View with any strategy")
            return False

        except Exception as e:
            logger.error(f"Failed to enter Street View: {e}")
            return False

    def _enter_street_view_via_pegman(self) -> bool:
        """
        Enter Street View by dragging Pegman onto the map.

        Returns:
            True if successful
        """
        try:
            # First, we need to enable Street View layer to show blue lines
            # Try to find Pegman or Street View toggle button
            pegman_selectors = [
                (By.XPATH, "//button[contains(@aria-label, 'Pegman')]"),
                (By.XPATH, "//button[contains(@aria-label, 'Street View')]"),
                (By.XPATH, "//div[contains(@class, 'pegman')]"),
                (By.CSS_SELECTOR, ".widget-minimap-pegman"),
                (By.CSS_SELECTOR, "[data-control='pegman']"),
                (By.XPATH, "//button[contains(@class, 'pegman')]"),
            ]

            pegman = None
            for selector in pegman_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed():
                        pegman = element
                        logger.info(f"Found Pegman with selector: {selector}")
                        break
                except Exception:
                    continue

            if not pegman:
                logger.debug("Pegman not found, trying alternative method")
                return False

            # Get map canvas
            try:
                canvas = self.find_element(self.MAP_CANVAS, timeout=3)
            except Exception:
                canvas = self.driver.find_element(By.TAG_NAME, "body")

            # Drag Pegman to center of map
            actions = ActionChains(self.driver)
            actions.click_and_hold(pegman)
            actions.move_to_element(canvas)
            actions.release()
            actions.perform()

            time.sleep(2.5)

            if self._is_in_street_view():
                logger.info("Entered Street View via Pegman drag")
                return True

            return False

        except Exception as e:
            logger.debug(f"Pegman method failed: {e}")
            return False

    def _enter_street_view_via_click(self) -> bool:
        """
        Enter Street View by clicking directly on the map (works when Street View layer is visible).
        Uses single click on roads that have Street View coverage.

        Returns:
            True if successful
        """
        try:
            # Get map canvas
            try:
                canvas = self.find_element(self.MAP_CANVAS, timeout=3)
            except Exception:
                try:
                    canvas = self.driver.find_element(By.ID, "scene")
                except Exception:
                    canvas = self.driver.find_element(By.TAG_NAME, "body")

            canvas_width = canvas.size.get('width', 800)
            canvas_height = canvas.size.get('height', 600)

            # Positions to try - roads are typically in these areas
            # Using relative positions from center
            click_positions = [
                (0, 50),          # Slightly below center (main roads)
                (0, 100),         # Further below
                (100, 50),        # Right-bottom area
                (-100, 50),       # Left-bottom area
                (0, 0),           # Center
                (50, 0),          # Slightly right
                (-50, 0),         # Slightly left
                (0, -50),         # Above center
                (150, 100),       # Bottom-right
                (-150, 100),      # Bottom-left
            ]

            for x_offset, y_offset in click_positions:
                try:
                    # First try single click to see if it opens Street View preview
                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(canvas, x_offset, y_offset)
                    actions.click()
                    actions.perform()

                    time.sleep(1.0)

                    # Check if a Street View preview appeared
                    preview_selectors = [
                        (By.XPATH, "//div[contains(@class, 'widget-pane-content')]//img[contains(@src, 'streetview')]"),
                        (By.XPATH, "//a[contains(@href, 'layer=c')]"),
                        (By.XPATH, "//div[contains(@class, 'place-desc-streetview')]"),
                    ]

                    for selector in preview_selectors:
                        try:
                            preview = self.driver.find_element(*selector)
                            if preview.is_displayed():
                                preview.click()
                                time.sleep(2.0)
                                if self._is_in_street_view():
                                    logger.info(f"Entered Street View via preview click at ({x_offset}, {y_offset})")
                                    return True
                        except Exception:
                            continue

                    # Try double-click as fallback for this position
                    actions = ActionChains(self.driver)
                    actions.move_to_element_with_offset(canvas, x_offset, y_offset)
                    actions.double_click()
                    actions.perform()

                    time.sleep(2.0)

                    if self._is_in_street_view():
                        logger.info(f"Entered Street View via double-click at ({x_offset}, {y_offset})")
                        return True

                except Exception as e:
                    logger.debug(f"Click position ({x_offset}, {y_offset}) failed: {e}")
                    continue

            return False

        except Exception as e:
            logger.debug(f"Click method failed: {e}")
            return False

    def _enter_street_view_via_keyboard(self) -> bool:
        """
        Try to enter Street View using keyboard navigation.

        Returns:
            True if successful
        """
        try:
            # Focus on the map first
            try:
                canvas = self.find_element(self.MAP_CANVAS, timeout=3)
                canvas.click()
            except Exception:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.click()

            time.sleep(0.5)

            # Try pressing Enter which sometimes opens Street View at current location
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()

            time.sleep(2.0)

            if self._is_in_street_view():
                logger.info("Entered Street View via keyboard")
                return True

            return False

        except Exception as e:
            logger.debug(f"Keyboard method failed: {e}")
            return False

    def _is_in_street_view(self) -> bool:
        """
        Check if currently in Street View mode.

        Returns:
            True if in Street View, False otherwise
        """
        try:
            # Method 1: Check URL for Street View indicators
            current_url = self.driver.current_url
            if any(indicator in current_url for indicator in ["@", "!3m", "layer=c", "/streetview", "cbll="]):
                # Check for pano parameter which indicates Street View
                if "!1s" in current_url and "!2e" in current_url:
                    return True
                if "layer=c" in current_url:
                    return True

            # Method 2: Check for Street View specific UI elements
            street_view_indicators = [
                (By.XPATH, "//div[contains(@class, 'widget-scene-canvas-header')]"),
                (By.XPATH, "//div[@class='widget-scene']//canvas"),
                (By.XPATH, "//button[contains(@aria-label, 'Voltar ao mapa') or contains(@aria-label, 'Back to map')]"),
                (By.XPATH, "//div[contains(@class, 'scene-footer')]"),
                (By.XPATH, "//div[@id='titlecard']"),
                (By.XPATH, "//div[contains(@class, 'widget-titlecard')]"),
                (By.XPATH, "//canvas[contains(@class, 'widget-scene-canvas')]"),
                (By.CSS_SELECTOR, ".widget-scene-canvas"),
            ]

            for locator in street_view_indicators:
                try:
                    element = self.driver.find_element(*locator)
                    if element.is_displayed():
                        # Additional check: verify the canvas is large (Street View canvas is fullscreen-ish)
                        if 'canvas' in locator[1].lower() or 'scene' in locator[1].lower():
                            try:
                                height = element.size.get('height', 0)
                                if height > 200:  # Street View canvas should be large
                                    return True
                            except Exception:
                                pass
                        else:
                            return True
                except Exception:
                    continue

            # Method 3: Check for exit button
            exit_selectors = [
                (By.XPATH, "//button[contains(@aria-label, 'Voltar ao mapa')]"),
                (By.XPATH, "//button[contains(@aria-label, 'Back to map')]"),
                (By.XPATH, "//button[contains(@jsaction, 'pane.close') and ancestor::div[contains(@class, 'scene')]]"),
            ]

            for selector in exit_selectors:
                try:
                    if self.is_element_visible(selector, timeout=0.5):
                        return True
                except Exception:
                    continue

            return False

        except Exception as e:
            logger.debug(f"Error checking Street View status: {e}")
            return False

    def exit_street_view(self) -> bool:
        """
        Exit Street View mode.
        Tries multiple methods: exit button, Escape key, back navigation.

        Returns:
            True if successfully exited Street View
        """
        try:
            # Check if we're actually in Street View
            if not self._is_in_street_view():
                logger.info("Not in Street View mode, nothing to exit")
                return True

            # Method 1: Try clicking exit/back button
            exit_button_locators = [
                (By.XPATH, "//button[contains(@aria-label, 'Voltar ao mapa')]"),
                (By.XPATH, "//button[contains(@aria-label, 'Back to map')]"),
                (By.XPATH, "//button[contains(@aria-label, 'Fechar')]"),
                (By.XPATH, "//button[contains(@aria-label, 'Close')]"),
                (By.XPATH, "//button[contains(@jsaction, 'pane.close')]"),
                (By.XPATH, "//div[contains(@class, 'scene-footer')]//button"),
                (By.CSS_SELECTOR, "button.scene-footer-close-button"),
                self.STREET_VIEW_EXIT,
            ]

            for locator in exit_button_locators:
                try:
                    element = self.driver.find_element(*locator)
                    if element.is_displayed():
                        element.click()
                        logger.info(f"Clicked exit button: {locator}")
                        time.sleep(1.5)

                        if not self._is_in_street_view():
                            logger.info("Exited Street View via button")
                            return True
                except Exception:
                    continue

            # Method 2: Press Escape key multiple times
            actions = ActionChains(self.driver)
            for _ in range(3):
                actions.send_keys(Keys.ESCAPE)
                actions.perform()
                time.sleep(0.5)

                if not self._is_in_street_view():
                    logger.info("Exited Street View via Escape key")
                    return True

            # Method 3: Navigate back in browser history
            try:
                self.driver.back()
                time.sleep(1.5)

                if not self._is_in_street_view():
                    logger.info("Exited Street View via browser back")
                    return True
            except Exception:
                pass

            logger.warning("Could not exit Street View")
            return False

        except Exception as e:
            logger.error(f"Failed to exit Street View: {e}")
            return False

    def open_explore_menu(self) -> bool:
        """
        Open the 'Coisas a fazer' (Explore/Activities) menu.

        Returns:
            True if successfully opened the menu
        """
        try:
            # Try to find and click the explore button
            if self.is_element_visible(self.EXPLORE_BUTTON, timeout=5):
                self.click(self.EXPLORE_BUTTON)
                logger.info("Opened Explore/Coisas a fazer menu")
                time.sleep(0.5)
                return True

            logger.warning("Could not find Explore button")
            return False

        except Exception as e:
            logger.error(f"Failed to open Explore menu: {e}")
            return False

    def move_forward_street_view(self) -> bool:
        """
        Move forward in Street View mode.
        Tries multiple methods:
        1. Click on the road/path ahead (center of screen)
        2. Press W key (alternative forward key)
        3. Press Arrow Up key with proper focus

        Returns:
            True if successful
        """
        try:
            if not self._is_in_street_view():
                logger.warning("Not in Street View, cannot move forward")
                return False

            # Method 1: Click on the center-bottom area of the screen (road ahead)
            if self._move_forward_by_click():
                return True

            # Method 2: Press W key (WASD controls)
            if self._move_forward_by_key("w"):
                return True

            # Method 3: Press Arrow Up with proper focus
            if self._move_forward_by_key(Keys.ARROW_UP):
                return True

            logger.warning("Could not move forward in Street View")
            return False

        except Exception as e:
            logger.error(f"Error moving forward in Street View: {e}")
            return False

    def _move_forward_by_click(self) -> bool:
        """
        Move forward by clicking on the road ahead in Street View.

        Returns:
            True if successful
        """
        try:
            # Find the Street View canvas
            canvas_selectors = [
                (By.CSS_SELECTOR, "canvas.widget-scene-canvas"),
                (By.CSS_SELECTOR, "#scene canvas"),
                (By.CSS_SELECTOR, ".widget-scene canvas"),
                (By.XPATH, "//div[contains(@class, 'widget-scene')]//canvas"),
            ]

            canvas = None
            for selector in canvas_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed() and element.size.get('height', 0) > 200:
                        canvas = element
                        logger.debug(f"Found Street View canvas: {selector}")
                        break
                except Exception:
                    continue

            if not canvas:
                logger.debug("Could not find Street View canvas for click")
                return False

            # Get canvas dimensions
            width = canvas.size.get('width', 800)
            height = canvas.size.get('height', 600)

            # Click on the center-bottom area (where the road ahead typically is)
            # This is usually around 50-60% down from the center
            click_y_offset = int(height * 0.15)  # Slightly below center

            actions = ActionChains(self.driver)
            actions.move_to_element(canvas)
            actions.move_by_offset(0, click_y_offset)
            actions.click()
            actions.perform()

            logger.info("Moved forward by clicking on road ahead")
            time.sleep(0.5)
            return True

        except Exception as e:
            logger.debug(f"Click forward failed: {e}")
            return False

    def _move_forward_by_key(self, key) -> bool:
        """
        Move forward by pressing a key (W or Arrow Up).

        Args:
            key: The key to press (Keys.ARROW_UP or "w")

        Returns:
            True if successful
        """
        try:
            # First, ensure the Street View canvas has focus
            canvas_selectors = [
                (By.CSS_SELECTOR, "canvas.widget-scene-canvas"),
                (By.CSS_SELECTOR, "#scene canvas"),
                (By.CSS_SELECTOR, ".widget-scene canvas"),
                (By.XPATH, "//div[contains(@class, 'widget-scene')]//canvas"),
                (By.CSS_SELECTOR, "#scene"),
                (By.CSS_SELECTOR, ".widget-scene"),
            ]

            focused = False
            for selector in canvas_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed():
                        # Click to focus
                        actions = ActionChains(self.driver)
                        actions.move_to_element(element)
                        actions.click()
                        actions.perform()
                        focused = True
                        time.sleep(0.2)
                        break
                except Exception:
                    continue

            if not focused:
                # Fallback: click on body
                self.driver.find_element(By.TAG_NAME, "body").click()
                time.sleep(0.2)

            # Now send the key
            actions = ActionChains(self.driver)
            actions.send_keys(key)
            actions.perform()

            key_name = "W" if key == "w" else "Arrow Up"
            logger.info(f"Moved forward using {key_name} key")
            time.sleep(0.3)
            return True

        except Exception as e:
            logger.debug(f"Key forward failed: {e}")
            return False

    def rotate_street_view(self, direction: str) -> bool:
        """
        Rotate camera in Street View mode.

        Args:
            direction: 'left', 'right', 'up', or 'down'

        Returns:
            True if successful
        """
        try:
            if not self._is_in_street_view():
                logger.warning("Not in Street View, cannot rotate")
                return False

            direction_keys = {
                "left": Keys.ARROW_LEFT,
                "right": Keys.ARROW_RIGHT,
                "up": Keys.ARROW_UP,
                "down": Keys.ARROW_DOWN
            }

            key = direction_keys.get(direction.lower())
            if not key:
                logger.error(f"Invalid direction: {direction}")
                return False

            # Focus on the Street View canvas first
            canvas_selectors = [
                (By.CSS_SELECTOR, "canvas.widget-scene-canvas"),
                (By.CSS_SELECTOR, "#scene canvas"),
                (By.CSS_SELECTOR, ".widget-scene canvas"),
            ]

            for selector in canvas_selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed():
                        actions = ActionChains(self.driver)
                        actions.move_to_element(element)
                        actions.click()
                        actions.perform()
                        time.sleep(0.1)
                        break
                except Exception:
                    continue

            # Send arrow keys multiple times for visible rotation
            actions = ActionChains(self.driver)
            for _ in range(3):
                actions.send_keys(key)
            actions.perform()

            logger.info(f"Rotated Street View camera {direction}")
            return True

        except Exception as e:
            logger.error(f"Error rotating Street View: {e}")
            return False
