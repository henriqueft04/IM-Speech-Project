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
            time.sleep(0.3)  # Brief pause between actions

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
            time.sleep(0.3)  # Brief pause between actions

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
            time.sleep(0.3)  # Brief pause between actions

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
            time.sleep(0.3)  # Brief pause between actions

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
            time.sleep(0.3)  # Brief pause between actions

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
            time.sleep(0.3)  # Brief pause between actions

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
            time.sleep(0.3)  # Brief pause between actions

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
            time.sleep(0.3)  # Brief pause between actions

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
