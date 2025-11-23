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
        # Validate required entities
        is_valid, error_msg = self.validate_entities(context, ["location"])
        if not is_valid:
            return IntentResponse(
                success=False,
                message="Não percebi a localização. Que lugar queres procurar?",
                data={"error": error_msg}
            )

        location_query = context.get_entity("location")
        self.logger.info(f"Searching for location: {location_query}")

        try:
            # Use MapsHomePage to perform search
            home_page = MapsHomePage(context.driver)
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
        # Validate required entities
        is_valid, error_msg = self.validate_entities(context, ["destination"])
        if not is_valid:
            return IntentResponse(
                success=False,
                message="Para onde queres ir?",
                data={"error": error_msg}
            )

        destination = context.get_entity("destination")
        origin = context.get_entity("origin")  # Optional
        transport_mode_str = context.get_entity("transport_mode")  # Optional

        self.logger.info(
            f"Getting directions: {origin or 'current location'} -> {destination}"
        )

        try:
            # Use MapsHomePage to set directions
            home_page = MapsHomePage(context.driver)
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
