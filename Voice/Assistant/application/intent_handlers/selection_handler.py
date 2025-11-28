"""
Intent handlers for selecting items from search results.
Handles ordinal selection (first, second, third, etc.)
"""

import logging
from typing import Optional

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter
from infrastructure.page_objects import MapsSearchResultsPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


@IntentRouter.register("select_place")
class SelectPlaceHandler(BaseIntentHandler):
    """Handler for selecting a place from search results."""

    supported_intents = ["select_place"]
    requires_confirmation = False
    confidence_threshold = 0.75

    # Mapping of ordinal words to numbers (Portuguese)
    ORDINAL_MAP = {
        "primeiro": 1,
        "primeira": 1,
        "segundo": 2,
        "segunda": 2,
        "terceiro": 3,
        "terceira": 3,
        "quarto": 4,
        "quarta": 4,
        "quinto": 5,
        "quinta": 5,
        "sexto": 6,
        "sexta": 6,
        "sétimo": 7,
        "sétima": 7,
        "oitavo": 8,
        "oitava": 8,
        "nono": 9,
        "nona": 9,
        "décimo": 10,
        "décima": 10,
        # English
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
        "sixth": 6,
        "seventh": 7,
        "eighth": 8,
        "ninth": 9,
        "tenth": 10,
    }

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Select a place from search results.

        Args:
            context: Intent context with ordinal entity

        Returns:
            IntentResponse confirming selection
        """
        # Get ordinal (e.g., "primeiro", "1", "first")
        ordinal_str = context.get_entity("ordinal")

        if not ordinal_str:
            return IntentResponse(
                success=False,
                message="Qual resultado queres? Diz 'primeiro', 'segundo', etc."
            )

        # Convert ordinal to number
        index = self._parse_ordinal(ordinal_str)

        if index is None or index < 1:
            return IntentResponse(
                success=False,
                message=f"Não percebi '{ordinal_str}'. Usa 'primeiro', 'segundo', etc."
            )

        self.logger.info(f"Selecting result #{index}")

        try:
            results_page = MapsSearchResultsPage(context.driver)

            # Click the result
            success = results_page.select_result_by_index(index - 1)  # 0-indexed

            if not success:
                return IntentResponse(
                    success=False,
                    message=f"Não encontrei o resultado número {index}. Quantos resultados existem?"
                )

            # Wait for place page to load
            from infrastructure.page_objects import MapsPlacePage
            place_page = MapsPlacePage(context.driver)

            if place_page.wait_for_place_details(timeout=5):
                place_name = place_page.get_place_name()
                return IntentResponse(
                    success=True,
                    message=f"Selecionei {place_name}",
                    data={"place_name": place_name, "index": index}
                )
            else:
                return IntentResponse(
                    success=True,
                    message=f"Selecionei o resultado número {index}"
                )

        except Exception as e:
            self.logger.error(f"Error selecting place: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message=f"Ocorreu um erro ao selecionar o resultado número {index}",
                data={"error": str(e)}
            )

    def _parse_ordinal(self, ordinal_str: str) -> Optional[int]:
        """
        Parse ordinal string to number.

        Args:
            ordinal_str: Ordinal string (e.g., "primeiro", "1", "first")

        Returns:
            Number (1-indexed) or None if invalid
        """
        ordinal_lower = ordinal_str.lower().strip()

        # Check if it's a direct number
        if ordinal_lower.isdigit():
            return int(ordinal_lower)

        # Check mapped ordinals
        return self.ORDINAL_MAP.get(ordinal_lower)


@IntentRouter.register("select_alternative_route")
class SelectAlternativeRouteHandler(BaseIntentHandler):
    """Handler for selecting alternative route options."""

    supported_intents = ["select_alternative_route"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Select an alternative route from the directions panel.

        Args:
            context: Intent context with ordinal entity

        Returns:
            IntentResponse confirming route selection
        """
        ordinal_str = context.get_entity("ordinal")

        # Check for keywords in the full text to determine intent
        full_text = ""
        if context.metadata and "text" in context.metadata:
            full_text = context.metadata["text"].strip().lower()

        # If no ordinal specified, interpret based on keywords
        if not ordinal_str:
            # Keywords for first/main route
            if any(word in full_text for word in ["anterior", "principal", "original", "primeira", "primeiro"]):
                route_index = 0  # First route (main route)
            else:
                # Default to second route for "outra rota", "alternativa", etc.
                route_index = 1  # Second route (first alternative)
        else:
            # Parse which route to select
            route_index = self._parse_route_number(ordinal_str)

        self.logger.info(f"Selecting alternative route #{route_index}")

        try:
            # XPath for route options in directions panel
            # Based on actual Google Maps HTML structure
            route_xpaths = [
                # Try specific ID with data-trip-index attribute (most reliable)
                f"//div[@id='section-directions-trip-{route_index}' and @data-trip-index='{route_index}']",
                # Try just the ID
                f"//div[@id='section-directions-trip-{route_index}']",
                # Try using data-trip-index alone
                f"//div[@data-trip-index='{route_index}']",
                # Try role-based selection
                f"//div[@data-trip-index='{route_index}' and (@role='button' or @role='link')]",
                # Fallback: try nth child of parent
                f"(//div[starts-with(@id, 'section-directions-trip-')])[{route_index + 1}]",
            ]

            route_selected = False
            for xpath in route_xpaths:
                try:
                    route_elem = context.driver.find_element(By.XPATH, xpath)
                    if route_elem.is_displayed():
                        # Scroll element into view before clicking
                        context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", route_elem)
                        import time
                        time.sleep(0.3)  # Brief wait for scroll

                        route_elem.click()
                        route_selected = True
                        self.logger.info(f"Clicked route option {route_index} using xpath: {xpath}")
                        break
                    else:
                        self.logger.debug(f"Element found but not displayed: {xpath}")
                except Exception as e:
                    self.logger.debug(f"XPath {xpath} failed: {e}")
                    continue

            if not route_selected:
                return IntentResponse(
                    success=False,
                    message="Não encontrei rotas alternativas. Pede direções primeiro."
                )

            return IntentResponse(
                success=True,
                message=f"Selecionei a rota número {route_index}"
            )

        except Exception as e:
            self.logger.error(f"Error selecting route: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao selecionar a rota alternativa",
                data={"error": str(e)}
            )

    def _parse_route_number(self, ordinal_str: str) -> int:
        """Parse route number from ordinal string."""
        ordinal_lower = ordinal_str.lower().strip()

        # Direct number (assume 1-indexed from user, convert to 0-indexed)
        if ordinal_lower.isdigit():
            num = int(ordinal_lower)
            return num - 1 if num > 0 else 0  # Convert 1->0, 2->1, 3->2

        # Ordinal words (map to 0-indexed route numbers)
        ordinals = {
            "primeiro": 0, "primeira": 0,  # First route = index 0
            "segundo": 1, "segunda": 1,    # Second route = index 1
            "terceiro": 2, "terceira": 2,  # Third route = index 2
            "first": 0, "second": 1, "third": 2
        }

        return ordinals.get(ordinal_lower, 1)  # Default to route 1 (second route)
