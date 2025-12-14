"""
Intent handler for gesture-based intents.
Handles gestures like selecting filters, swiping, etc.
"""

import logging

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter
from infrastructure.page_objects import MapsHomePage

logger = logging.getLogger(__name__)


@IntentRouter.register("gesture_restaurants")
class RestaurantsFilterHandler(BaseIntentHandler):
    """Handler for selecting restaurants filter via gesture."""

    supported_intents = ["gesture_restaurants"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Select the restaurants filter on Google Maps.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Click on the restaurants filter button
            # You may need to adjust the selector based on Google Maps UI
            home_page.click_filter_button("Restaurantes")

            return IntentResponse(
                success=True,
                message="A mostrar restaurantes na área"
            )

        except Exception as e:
            self.logger.error(f"Error selecting restaurants filter: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao selecionar restaurantes",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_hotels")
class HotelsFilterHandler(BaseIntentHandler):
    """Handler for selecting hotels filter via gesture."""

    supported_intents = ["gesture_hotels"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Select the hotels filter on Google Maps.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.click_filter_button("Hotéis")

            return IntentResponse(
                success=True,
                message="A mostrar hotéis na área"
            )

        except Exception as e:
            self.logger.error(f"Error selecting hotels filter: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao selecionar hotéis",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_gas_stations")
class GasStationsFilterHandler(BaseIntentHandler):
    """Handler for selecting gas stations filter via gesture."""

    supported_intents = ["gesture_gas_stations"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Select the gas stations filter on Google Maps.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.click_filter_button("Postos de combustível")

            return IntentResponse(
                success=True,
                message="A mostrar postos de combustível na área"
            )

        except Exception as e:
            self.logger.error(f"Error selecting gas stations filter: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao selecionar postos de combustível",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_swipe_left")
class SwipeLeftHandler(BaseIntentHandler):
    """Handler for swipe left gesture."""

    supported_intents = ["gesture_swipe_left"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe left gesture - e.g., go back or pan map left.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            # Pan the map to the left
            home_page.pan_map(direction="left")

            return IntentResponse(
                success=True,
                message="A mover para a esquerda"
            )

        except Exception as e:
            self.logger.error(f"Error handling swipe left: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_swipe_right")
class SwipeRightHandler(BaseIntentHandler):
    """Handler for swipe right gesture."""

    supported_intents = ["gesture_swipe_right"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe right gesture - e.g., pan map right.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.pan_map(direction="right")

            return IntentResponse(
                success=True,
                message="A mover para a direita"
            )

        except Exception as e:
            self.logger.error(f"Error handling swipe right: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )

@IntentRouter.register("gesture_swipe_up")
class SwipeUpHandler(BaseIntentHandler):
    """Handler for swipe up gesture."""

    supported_intents = ["gesture_swipe_up"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe up gesture - pan map up.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.pan_map(direction="up")

            return IntentResponse(
                success=True,
                message="A mover para cima"
            )

        except Exception as e:
            self.logger.error(f"Error handling swipe up: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )

@IntentRouter.register("gesture_swipe_down")
class SwipeDownHandler(BaseIntentHandler):
    """Handler for swipe down gesture."""

    supported_intents = ["gesture_swipe_down"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe down gesture - pan map down.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.pan_map(direction="down")

            return IntentResponse(
                success=True,
                message="A mover para baixo"
            )

        except Exception as e:
            self.logger.error(f"Error handling swipe down: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )

@IntentRouter.register("gesture_zoom_in")
class GestureZoomInHandler(BaseIntentHandler):
    """Handler for zoom in gesture (e.g., pinch out)."""

    supported_intents = ["gesture_zoom_in"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle zoom in gesture.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.zoom_in(clicks=2)

            return IntentResponse(
                success=True,
                message="A aproximar"
            )

        except Exception as e:
            self.logger.error(f"Error zooming in: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao aproximar",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_zoom_out")
class GestureZoomOutHandler(BaseIntentHandler):
    """Handler for zoom out gesture (e.g., pinch in)."""

    supported_intents = ["gesture_zoom_out"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle zoom out gesture.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.zoom_out(clicks=2)

            return IntentResponse(
                success=True,
                message="A afastar"
            )

        except Exception as e:
            self.logger.error(f"Error zooming out: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao afastar",
                data={"error": str(e)}
            )
