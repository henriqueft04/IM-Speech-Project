"""
Intent handler for map control intents.
Handles zoom, map type, traffic, and recenter.
"""

import logging

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter
from infrastructure.page_objects import MapsHomePage
from domain import MapType, ZoomLevel

logger = logging.getLogger(__name__)


@IntentRouter.register("zoom_in")
class ZoomInHandler(BaseIntentHandler):
    """Handler for zooming in on the map."""

    supported_intents = ["zoom_in"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom in on the map.

        Args:
            context: Intent context with optional zoom_level entity

        Returns:
            IntentResponse
        """
        zoom_level_str = context.get_entity("zoom_level")

        try:
            # Determine zoom clicks based on level
            if zoom_level_str:
                zoom_level = ZoomLevel.from_string(zoom_level_str)
                clicks = zoom_level.value
            else:
                clicks = 2  # Default

            home_page = MapsHomePage(context.driver)
            home_page.zoom_in(clicks=clicks)

            level_text = f" {zoom_level_str}" if zoom_level_str else ""
            return IntentResponse(
                success=True,
                message=f"A aproximar{level_text}"
            )

        except Exception as e:
            self.logger.error(f"Error zooming in: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao aproximar",
                data={"error": str(e)}
            )


@IntentRouter.register("zoom_out")
class ZoomOutHandler(BaseIntentHandler):
    """Handler for zooming out on the map."""

    supported_intents = ["zoom_out"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Zoom out on the map.

        Args:
            context: Intent context with optional zoom_level entity

        Returns:
            IntentResponse
        """
        zoom_level_str = context.get_entity("zoom_level")

        try:
            # Determine zoom clicks based on level
            if zoom_level_str:
                zoom_level = ZoomLevel.from_string(zoom_level_str)
                clicks = zoom_level.value
            else:
                clicks = 2  # Default

            home_page = MapsHomePage(context.driver)
            home_page.zoom_out(clicks=clicks)

            level_text = f" {zoom_level_str}" if zoom_level_str else ""
            return IntentResponse(
                success=True,
                message=f"A afastar{level_text}"
            )

        except Exception as e:
            self.logger.error(f"Error zooming out: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao afastar",
                data={"error": str(e)}
            )

@IntentRouter.register("change_map_type")
class ChangeMapTypeHandler(BaseIntentHandler):
    """Handler for changing map type (satellite, terrain, default)."""

    supported_intents = ["change_map_type"]
    requires_confirmation = False
    confidence_threshold = 0.75

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Change the map type.

        Args:
            context: Intent context with map_type entity

        Returns:
            IntentResponse
        """
        # Validate required entities
        is_valid, error_msg = self.validate_entities(context, ["map_type"])
        if not is_valid:
            return IntentResponse(
                success=False,
                message="Que tipo de mapa queres? Satélite, terreno, ou normal?",
                data={"error": error_msg}
            )

        map_type_str = context.get_entity("map_type")

        try:
            map_type = MapType.from_string(map_type_str)
            home_page = MapsHomePage(context.driver)
            success = home_page.change_map_type(map_type)

            if not success:
                return IntentResponse(
                    success=False,
                    message=f"Desculpa, não consegui mudar para vista de {map_type.value}"
                )

            return IntentResponse(
                success=True,
                message=f"Vista alterada para {map_type.value}"
            )

        except ValueError as e:
            return IntentResponse(
                success=False,
                message=f"Não reconheço o tipo de mapa '{map_type_str}'",
                data={"error": str(e)}
            )
        except Exception as e:
            self.logger.error(f"Error changing map type: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao mudar o tipo de mapa",
                data={"error": str(e)}
            )





@IntentRouter.register("recenter_map")
class RecenterMapHandler(BaseIntentHandler):
    """Handler for recentering map to current location."""

    supported_intents = ["recenter_map"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Recenter map to current location.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            success = home_page.recenter_map()

            if not success:
                return IntentResponse(
                    success=False,
                    message="Desculpa, não consegui recentrar o mapa"
                )

            return IntentResponse(
                success=True,
                message="Mapa recentrado na tua localização"
            )

        except Exception as e:
            self.logger.error(f"Error recentering map: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao recentrar o mapa",
                data={"error": str(e)}
            )
