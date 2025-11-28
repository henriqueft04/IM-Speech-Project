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
        Recenter map to current location or specific place.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            # Check if user specified a location to center on
            location = context.get_entity("location") or context.get_entity("destination")

            # If no entity, try using full text
            if not location and context.metadata and "text" in context.metadata:
                full_text = context.metadata["text"].strip().lower()
                # Remove "centrar", "em", etc. to extract location
                for word in ["centrar", "central", "em", "no", "na"]:
                    full_text = full_text.replace(word, "").strip()
                if full_text:
                    location = full_text

            if location:
                # Center on specific location by searching for it
                self.logger.info(f"Centering map on location: {location}")
                success = home_page.search(location)
                if success:
                    return IntentResponse(
                        success=True,
                        message=f"Mapa centrado em {location}"
                    )
            else:
                # Center on user's current GPS location
                success = home_page.recenter_map()
                if success:
                    return IntentResponse(
                        success=True,
                        message="Mapa recentrado na tua localização"
                    )

            return IntentResponse(
                success=False,
                message="Desculpa, não consegui recentrar o mapa"
            )

        except Exception as e:
            self.logger.error(f"Error recentering map: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao recentrar o mapa",
                data={"error": str(e)}
            )


@IntentRouter.register("show_traffic")
class ShowTrafficHandler(BaseIntentHandler):
    """Handler for showing traffic layer on the map."""

    supported_intents = ["show_traffic"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Show traffic layer on the map.

        Returns:
            IntentResponse confirming traffic display
        """
        self.logger.info("Showing traffic layer")

        try:
            home_page = MapsHomePage(context.driver)
            success = home_page.toggle_traffic_layer(show=True)

            if not success:
                return IntentResponse(
                    success=False,
                    message="Não consegui mostrar o trânsito. Tenta outra vez."
                )

            return IntentResponse(
                success=True,
                message="A mostrar trânsito no mapa"
            )

        except Exception as e:
            self.logger.error(f"Error showing traffic: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao mostrar o trânsito",
                data={"error": str(e)}
            )


@IntentRouter.register("hide_traffic")
class HideTrafficHandler(BaseIntentHandler):
    """Handler for hiding traffic layer from the map."""

    supported_intents = ["hide_traffic"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Hide traffic layer from the map.

        Returns:
            IntentResponse confirming traffic removal
        """
        self.logger.info("Hiding traffic layer")

        try:
            home_page = MapsHomePage(context.driver)
            success = home_page.toggle_traffic_layer(show=False)

            if not success:
                return IntentResponse(
                    success=False,
                    message="Não consegui esconder o trânsito. Tenta outra vez."
                )

            return IntentResponse(
                success=True,
                message="Trânsito escondido"
            )

        except Exception as e:
            self.logger.error(f"Error hiding traffic: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao esconder o trânsito",
                data={"error": str(e)}
            )


@IntentRouter.register("center_location")
class CenterLocationHandler(BaseIntentHandler):
    """Handler for centering map on a specific location."""

    supported_intents = ["center_location"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Center the map on a specific location.

        Args:
            context: Intent context with location entity

        Returns:
            IntentResponse confirming map centered
        """
        # Try to get location from either 'location' or 'destination' entity
        location = context.get_entity("location") or context.get_entity("destination")

        if not location:
            return IntentResponse(
                success=False,
                message="Em que lugar queres centrar o mapa?"
            )

        self.logger.info(f"Centering map on: {location}")

        try:
            home_page = MapsHomePage(context.driver)

            # Search for the location
            success = home_page.search(location)

            if not success:
                return IntentResponse(
                    success=False,
                    message=f"Não consegui encontrar {location}"
                )

            return IntentResponse(
                success=True,
                message=f"Centrado em {location}",
                data={"location": location}
            )

        except Exception as e:
            self.logger.error(f"Error centering on location: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message=f"Ocorreu um erro ao centrar em {location}",
                data={"error": str(e)}
            )
