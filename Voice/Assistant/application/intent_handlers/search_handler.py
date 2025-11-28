"""
Intent handler for search and navigation intents.
Handles search_location, get_directions, and start_navigation.
"""

import logging
import time

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter
from infrastructure.page_objects import (
    MapsHomePage,
    MapsSearchResultsPage,
    MapsPlacePage
)
from domain import TransportMode

logger = logging.getLogger(__name__)


@IntentRouter.register("search_location")
class SearchLocationHandler(BaseIntentHandler):
    """Handler for searching locations."""

    supported_intents = ["search_location"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Execute location search.

        Args:
            context: Intent context with location entity

        Returns:
            IntentResponse with search results
        """
        # For search_location intent, always use the full text
        # This preserves queries like "restaurantes perto da Lixa"
        # Entity extraction often splits this incorrectly
        location_query = None

        if context.metadata and "text" in context.metadata:
            location_query = context.metadata["text"].strip()
            self.logger.info(f"Using full text as search query: {location_query}")
        else:
            # Fallback to location entity if no text available
            location_query = context.get_entity("location")

        # Final validation
        if not location_query or len(location_query) <= 2:
            return IntentResponse(
                success=False,
                message="Não percebi a localização. Que lugar queres procurar?",
                data={"error": "invalid_location"}
            )

        self.logger.info(f"Searching for: {location_query}")

        try:
            # Use MapsHomePage to perform search
            home_page = MapsHomePage(context.driver)

            # Reset map state to close any open panels (directions, place details, etc.)
            try:
                home_page.reset_map_state()
                self.logger.info("Reset map state before new search")
            except:
                pass  # Ignore if reset fails

            search_success = home_page.search(location_query)

            if not search_success:
                return IntentResponse(
                    success=False,
                    message=f"Desculpa, não consegui procurar {location_query}. Tenta outra vez."
                )

            # Check if Google Maps went directly to a place page or to search results
            # Give Google Maps a moment to load the page
            time.sleep(1)

            # Try to detect if we're on a place page (direct match)
            place_page = MapsPlacePage(context.driver)
            is_place_page = place_page.wait_for_place_details(timeout=2)

            if is_place_page:
                # We went directly to a place page (exact match)
                place_name = place_page.get_place_name()
                self.logger.info(f"Went directly to place page: {place_name}")

                return IntentResponse(
                    success=True,
                    message=f"Encontrei {place_name}",
                    data={"direct_match": True, "place_name": place_name}
                )

            # We're on a search results page
            results_page = MapsSearchResultsPage(context.driver)
            results_page.wait_for_results(timeout=10)

            search_result = results_page.get_top_results(n=3)

            if len(search_result) == 0:
                return IntentResponse(
                    success=True,
                    message=f"Não consegui encontrar resultados para {location_query}."
                )

            # Format results for TTS
            result_names = [loc.name for loc in search_result.locations]
            if len(result_names) == 1:
                message = f"Encontrei {result_names[0]}"
            else:
                message = f"Encontrei {len(result_names)} resultados: " + ", ".join(result_names)

            return IntentResponse(
                success=True,
                message=message,
                data={"search_results": search_result}
            )

        except Exception as e:
            self.logger.error(f"Error searching for location: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message=f"Ocorreu um erro ao procurar {location_query}",
                data={"error": str(e)}
            )


@IntentRouter.register("get_directions")
class GetDirectionsHandler(BaseIntentHandler):
    """Handler for getting directions between locations."""

    supported_intents = ["get_directions"]
    requires_confirmation = False
    confidence_threshold = 0.75

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Get directions to a destination.

        Args:
            context: Intent context with destination and optional origin/transport_mode

        Returns:
            IntentResponse with directions
        """
        # Handle multiple destination entities (e.g., "da Lixa a Lisboa")
        # Access raw NLU data from metadata to get ALL entities
        origin = context.get_entity("origin")
        destination = context.get_entity("destination")

        # Check if we have multiple destinations in raw NLU data
        if context.metadata and "nlu" in context.metadata:
            import json
            try:
                nlu_data = json.loads(context.metadata["nlu"])
                raw_entities = nlu_data.get("entities", [])

                # Find all destination entities
                dest_entities = [e["value"] for e in raw_entities if e.get("entity") == "destination"]

                if len(dest_entities) >= 2 and not origin:
                    # Two destinations = origin + destination pattern
                    origin = dest_entities[0]
                    destination = dest_entities[1]
                    self.logger.info(f"Extracted from dual destinations: {origin} -> {destination}")
                elif len(dest_entities) == 1:
                    destination = dest_entities[0]
            except Exception as e:
                self.logger.warning(f"Failed to parse NLU data: {e}")

        # If no entity extracted, try to use the entire text as destination
        if not destination and context.metadata:
            text = context.metadata.get("text", "").strip()
            # Use text if it's not empty and not a common word
            if text and len(text) > 2:
                destination = text
                self.logger.info(f"Using full text as destination: {destination}")

        # Validate we have a destination
        if not destination:
            return IntentResponse(
                success=False,
                message="Para onde queres ir?",
                data={"error": "missing_destination"}
            )
        transport_mode_str = context.get_entity("transport_mode")  # Optional

        self.logger.info(
            f"Getting directions: {origin or 'current location'} -> {destination}"
        )

        # Don't send any intermediate messages - only send final result
        # This prevents confusing error messages from appearing before success

        try:
            home_page = MapsHomePage(context.driver)

            # Reset map state to close any open panels (directions, place details, etc.)
            try:
                home_page.reset_map_state()
                self.logger.info("Reset map state before new directions")
            except:
                pass  # Ignore if reset fails

            # Try to get directions directly
            directions_success = home_page.set_directions(
                destination=destination,
                origin=origin
            )

            if not directions_success:
                # Fallback: Search for the location first, then get directions
                self.logger.info(f"Direct directions failed, trying search first for: {destination}")

                search_success = home_page.search(destination)
                if search_success:
                    # Try to click Directions button from the place card
                    from infrastructure.page_objects import MapsPlacePage
                    place_page = MapsPlacePage(context.driver)

                    try:
                        # Wait for search results to load and check if we're on a place page
                        self.logger.info("Waiting for search results to load...")
                        if place_page.wait_for_place_details(timeout=8):
                            self.logger.info("On place page, clicking Directions button")

                            # Click the Directions button and wait for panel to open
                            place_page.click(place_page.DIRECTIONS_BUTTON)

                            # Wait for directions panel to appear by checking for destination input
                            if home_page.is_element_visible(home_page.DIRECTIONS_DEST_INPUT, timeout=5):
                                self.logger.info("Directions panel opened successfully")
                                directions_success = True
                            else:
                                self.logger.warning("Directions button clicked but panel didn't open")
                    except Exception as e:
                        self.logger.warning(f"Could not click place page Directions button: {e}")

                    # If that didn't work, try the original method
                    if not directions_success:
                        directions_success = home_page.set_directions(
                            destination=destination,
                            origin=origin
                        )

                if not directions_success:
                    return IntentResponse(
                        success=False,
                        message=f"Desculpa, não consegui obter direções para {destination}. Tenta outra vez."
                    )

            # Set transport mode if specified
            if transport_mode_str:
                try:
                    transport_mode = TransportMode.from_string(transport_mode_str)
                    self._set_transport_mode(home_page, transport_mode)
                    mode_text = f" de {transport_mode.value}"
                except ValueError:
                    self.logger.warning(f"Unknown transport mode: {transport_mode_str}")
                    mode_text = ""
            else:
                mode_text = ""

            origin_text = origin if origin else "a tua localização atual"
            message = f"A mostrar direções de {origin_text} para {destination}{mode_text}"

            return IntentResponse(
                success=True,
                message=message,
                data={
                    "origin": origin,
                    "destination": destination,
                    "transport_mode": transport_mode_str
                }
            )

        except Exception as e:
            self.logger.error(f"Error getting directions: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message=f"Ocorreu um erro ao obter direções para {destination}",
                data={"error": str(e)}
            )

    def _set_transport_mode(self, home_page: MapsHomePage, mode: TransportMode):
        """
        Set the transport mode for directions.

        Args:
            home_page: MapsHomePage instance
            mode: TransportMode enum value
        """
        mode_map = {
            TransportMode.DRIVING: home_page.DRIVING_MODE,
            TransportMode.WALKING: home_page.WALKING_MODE,
            TransportMode.TRANSIT: home_page.TRANSIT_MODE,
            TransportMode.CYCLING: home_page.CYCLING_MODE,
        }

        locator = mode_map.get(mode)
        if locator:
            home_page.select_transport_mode(locator)
            self.logger.info(f"Set transport mode to: {mode.value}")


@IntentRouter.register("start_navigation")
class StartNavigationHandler(BaseIntentHandler):
    """Handler for starting turn-by-turn navigation."""

    supported_intents = ["start_navigation"]
    requires_confirmation = True  # Confirm before starting navigation
    confidence_threshold = 0.80

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Start navigation for the current route.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        self.logger.info("Starting navigation")

        try:
            home_page = MapsHomePage(context.driver)
            nav_success = home_page.start_navigation()

            if not nav_success:
                return IntentResponse(
                    success=False,
                    message="Desculpa, não consegui iniciar a navegação. Certifica-te que tens direções definidas."
                )

            return IntentResponse(
                success=True,
                message="Navegação iniciada. Boa viagem!"
            )

        except Exception as e:
            self.logger.error(f"Error starting navigation: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao iniciar a navegação",
                data={"error": str(e)}
            )


@IntentRouter.register("stop_navigation")
class StopNavigationHandler(BaseIntentHandler):
    """Handler for stopping navigation."""

    supported_intents = ["stop_navigation"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Stop navigation.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        self.logger.info("Stopping navigation")

        try:
            # Press Escape key to exit navigation
            home_page = MapsHomePage(context.driver)
            home_page.send_keyboard_shortcut("ESCAPE")

            return IntentResponse(
                success=True,
                message="Navegação parada"
            )

        except Exception as e:
            self.logger.error(f"Error stopping navigation: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao parar a navegação",
                data={"error": str(e)}
            )
