"""
Intent handler for multimodal fusion intents.
Handles complementary fusion of speech and gesture modalities.
"""

import logging
import time

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter
from application.services.error_handler import handle_map_control_error
from infrastructure.page_objects import MapsHomePage

logger = logging.getLogger(__name__)


@IntentRouter.register("ZOOM_IN_UP")
class ZoomInUpHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom in + swipe up."""

    supported_intents = ["ZOOM_IN_UP"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom in and pan map upward (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom in first
            home_page.zoom_in(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan up
            success = home_page.pan_map("up", times=3)

            return IntentResponse(
                success=success,
                message="A aproximar e mover para cima" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_IN_UP: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "aproximar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("ZOOM_IN_DOWN")
class ZoomInDownHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom in + swipe down."""

    supported_intents = ["ZOOM_IN_DOWN"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom in and pan map downward (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom in first
            home_page.zoom_in(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan down
            success = home_page.pan_map("down", times=3)

            return IntentResponse(
                success=success,
                message="A aproximar e mover para baixo" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_IN_DOWN: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "aproximar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("ZOOM_OUT_UP")
class ZoomOutUpHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom out + swipe up."""

    supported_intents = ["ZOOM_OUT_UP"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom out and pan map upward (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom out first
            home_page.zoom_out(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan up
            success = home_page.pan_map("up", times=3)

            return IntentResponse(
                success=success,
                message="A afastar e mover para cima" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_OUT_UP: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "afastar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("ZOOM_OUT_DOWN")
class ZoomOutDownHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom out + swipe down."""

    supported_intents = ["ZOOM_OUT_DOWN"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom out and pan map downward (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom out first
            home_page.zoom_out(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan down
            success = home_page.pan_map("down", times=3)

            return IntentResponse(
                success=success,
                message="A afastar e mover para baixo" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_OUT_DOWN: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "afastar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("ZOOM_IN_LEFT")
class ZoomInLeftHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom in + swipe left."""

    supported_intents = ["ZOOM_IN_LEFT"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom in and pan map left (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom in first
            home_page.zoom_in(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan left
            success = home_page.pan_map("left", times=3)

            return IntentResponse(
                success=success,
                message="A aproximar e mover para a esquerda" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_IN_LEFT: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "aproximar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("ZOOM_IN_RIGHT")
class ZoomInRightHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom in + swipe right."""

    supported_intents = ["ZOOM_IN_RIGHT"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom in and pan map right (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom in first
            home_page.zoom_in(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan right
            success = home_page.pan_map("right", times=3)

            return IntentResponse(
                success=success,
                message="A aproximar e mover para a direita" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_IN_RIGHT: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "aproximar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("ZOOM_OUT_LEFT")
class ZoomOutLeftHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom out + swipe left."""

    supported_intents = ["ZOOM_OUT_LEFT"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom out and pan map left (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom out first
            home_page.zoom_out(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan left
            success = home_page.pan_map("left", times=3)

            return IntentResponse(
                success=success,
                message="A afastar e mover para a esquerda" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_OUT_LEFT: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "afastar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("ZOOM_OUT_RIGHT")
class ZoomOutRightHandler(BaseIntentHandler):
    """Handler for complementary fusion: zoom out + swipe right."""

    supported_intents = ["ZOOM_OUT_RIGHT"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom out and pan map right (combined action).
        This implements complementary fusion behavior.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute zoom out first
            home_page.zoom_out(clicks=2)
            time.sleep(0.1)  # Brief pause between actions (optimized)

            # Then pan right
            success = home_page.pan_map("right", times=3)

            return IntentResponse(
                success=success,
                message="A afastar e mover para a direita" if success else "Não consegui completar a ação"
            )

        except Exception as e:
            self.logger.error(f"Error in ZOOM_OUT_RIGHT: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "afastar e mover")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


# ============================================================================
# New Complementary Fusion Handlers - 2026
# ============================================================================


@IntentRouter.register("directions_public_transport")
class DirectionsPublicTransportHandler(BaseIntentHandler):
    """Handler for complementary fusion: get directions + transports gesture."""

    supported_intents = ["directions_public_transport"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Get directions and set transport mode to public transport (combined action).
        Voice: "como ir para Lisboa" + Gesture: TRANSPORTS

        Args:
            context: Intent context with destination entity from speech

        Returns:
            IntentResponse
        """
        try:
            from application.intent_handlers.search_handler import GetDirectionsHandler
            from domain import TransportMode

            home_page = MapsHomePage(context.driver)

            # Get destination from speech intent entities
            destination = context.get_entity("destination")

            if not destination and context.metadata:
                text = context.metadata.get("text", "").strip()
                if text and len(text) > 2:
                    destination = text

            if not destination:
                return IntentResponse(
                    success=False,
                    message="Para onde queres ir?",
                    data={"error": "missing_destination"}
                )

            # Execute get directions first
            self.logger.info(f"Getting directions to {destination}")

            # Reset map state
            try:
                home_page.reset_map_state()
            except:
                pass

            # Get directions
            directions_success = home_page.set_directions(destination=destination, origin=None)

            if not directions_success:
                # Fallback: search first then directions
                search_success = home_page.search(destination)
                if search_success:
                    from infrastructure.page_objects import MapsPlacePage
                    place_page = MapsPlacePage(context.driver)
                    if place_page.wait_for_place_details(timeout=5):
                        place_page.click(place_page.DIRECTIONS_BUTTON)
                        time.sleep(0.5)
                        directions_success = True

            if not directions_success:
                return IntentResponse(
                    success=False,
                    message=f"Não consegui obter direções para {destination}"
                )

            time.sleep(0.1)  # Brief pause (optimized)

            # Then set transport mode to public transport
            self.logger.info("Setting transport mode to public transport")
            home_page.select_transport_mode(home_page.TRANSIT_MODE)

            return IntentResponse(
                success=True,
                message=f"Direções de transportes públicos para {destination}"
            )

        except Exception as e:
            self.logger.error(f"Error in DIRECTIONS_PUBLIC_TRANSPORT: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "obter direções de transportes públicos")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("traffic_overview")
class TrafficOverviewHandler(BaseIntentHandler):
    """Handler for complementary fusion: show traffic + zoom out gesture."""

    supported_intents = ["traffic_overview"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Show traffic layer and zoom out for overview (combined action).
        Voice: "mostra tráfego" + Gesture: ZOOM_OUT

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Execute show traffic first
            self.logger.info("Showing traffic layer")
            home_page.toggle_traffic_layer(show=True)

            time.sleep(0.1)  # Brief pause (optimized)

            # Then zoom out for overview (3 clicks = good overview)
            self.logger.info("Zooming out for traffic overview")
            success = home_page.zoom_out(clicks=3)

            return IntentResponse(
                success=success,
                message="A mostrar visão geral do tráfego" if success else "Não consegui mostrar o tráfego"
            )

        except Exception as e:
            self.logger.error(f"Error in TRAFFIC_OVERVIEW: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "mostrar visão do tráfego")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("filter_restaurants_center")
class FilterRestaurantsCenterHandler(BaseIntentHandler):
    """Handler for complementary fusion: restaurants filter + recenter/select gesture."""

    supported_intents = ["filter_restaurants_center"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Activate restaurants filter and center on first result (combined action).
        Gesture: RESTAURANTS + Voice: "centrar" (or SWIPE_UP as center gesture)

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            from infrastructure.page_objects import MapsSearchResultsPage

            # Execute restaurant filter/search first
            self.logger.info("Searching for restaurants")
            search_success = home_page.search("restaurantes")

            if not search_success:
                return IntentResponse(
                    success=False,
                    message="Não consegui procurar restaurantes"
                )

            time.sleep(0.5)  # Wait for results to load

            # Then select/center on first result
            self.logger.info("Selecting first restaurant result")
            results_page = MapsSearchResultsPage(context.driver)

            try:
                results_page.wait_for_results(timeout=5)
                # Click on first result to center/select it
                first_result_success = results_page.click_result(index=0)

                if first_result_success:
                    time.sleep(0.3)  # Wait for place details to load
                    from infrastructure.page_objects import MapsPlacePage
                    place_page = MapsPlacePage(context.driver)

                    if place_page.wait_for_place_details(timeout=3):
                        place_name = place_page.get_place_name()
                        return IntentResponse(
                            success=True,
                            message=f"A mostrar {place_name}"
                        )

                return IntentResponse(
                    success=True,
                    message="A mostrar restaurantes próximos"
                )

            except Exception as results_error:
                self.logger.warning(f"Could not select first result: {results_error}")
                return IntentResponse(
                    success=True,
                    message="A mostrar restaurantes na área"
                )

        except Exception as e:
            self.logger.error(f"Error in FILTER_RESTAURANTS_CENTER: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "procurar e selecionar restaurante")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )


@IntentRouter.register("street_view_forward_continuous")
class StreetViewForwardContinuousHandler(BaseIntentHandler):
    """Handler for complementary fusion: forward gesture + navigation voice command."""

    supported_intents = ["street_view_forward_continuous"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Advance multiple times in Street View (continuous forward movement).
        Gesture: FORWARD + Voice: "avança" or "navega"

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Check if we're in Street View
            if not home_page._is_in_street_view():
                return IntentResponse(
                    success=False,
                    message="Preciso estar em Street View para avançar"
                )

            # Advance multiple times (simulate walking forward)
            self.logger.info("Advancing continuously in Street View")
            advances = 3  # Advance 3 times

            for i in range(advances):
                try:
                    home_page.street_view_move_forward()
                    time.sleep(0.15)  # Brief pause between advances (optimized)
                except Exception as advance_error:
                    self.logger.warning(f"Advance {i+1} failed: {advance_error}")
                    break

            return IntentResponse(
                success=True,
                message=f"A avançar em Street View"
            )

        except Exception as e:
            self.logger.error(f"Error in STREET_VIEW_FORWARD_CONTINUOUS: {e}", exc_info=True)
            user_message = handle_map_control_error(e, "avançar em Street View")
            return IntentResponse(
                success=False,
                message=user_message,
                data={"error": str(e)}
            )
