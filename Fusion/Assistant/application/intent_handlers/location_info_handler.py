"""
Intent handler for location information intents.
Handles place details, reviews, photos, and opening hours.
"""

import logging

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter
from infrastructure.page_objects import MapsPlacePage

logger = logging.getLogger(__name__)


@IntentRouter.register("show_place_details")
class ShowPlaceDetailsHandler(BaseIntentHandler):
    """Handler for showing place details."""

    supported_intents = ["show_place_details"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Show place details for the current location.

        Args:
            context: Intent context

        Returns:
            IntentResponse with place details
        """
        try:
            place_page = MapsPlacePage(context.driver)

            # Wait for place details to load
            if not place_page.wait_for_place_details(timeout=10):
                return IntentResponse(
                    success=False,
                    message="Por favor seleciona um lugar primeiro para ver os detalhes"
                )

            # Get place details
            details = place_page.get_place_details()

            # Format message
            message_parts = [details.location.name]

            if details.rating:
                message_parts.append(details.get_rating_text())

            if details.is_open_now is not None:
                status = "Open now" if details.is_open_now else "Closed"
                message_parts.append(status)

            if details.location.formatted_address:
                message_parts.append(details.location.formatted_address)

            message = ". ".join(message_parts)

            return IntentResponse(
                success=True,
                message=message,
                data={"place_details": details}
            )

        except Exception as e:
            self.logger.error(f"Error showing place details: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao obter os detalhes do lugar",
                data={"error": str(e)}
            )


@IntentRouter.register("show_reviews")
class ShowReviewsHandler(BaseIntentHandler):
    """Handler for showing place reviews."""

    supported_intents = ["show_reviews"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Show reviews for the current place.

        Args:
            context: Intent context

        Returns:
            IntentResponse with reviews
        """
        try:
            place_page = MapsPlacePage(context.driver)

            # Check if we're on a place page
            if not place_page.wait_for_place_details(timeout=5):
                return IntentResponse(
                    success=False,
                    message="Por favor seleciona um lugar primeiro para ver as avaliações"
                )

            # Navigate to reviews tab
            success = place_page.show_reviews()
            if not success:
                return IntentResponse(
                    success=False,
                    message="Desculpa, não consegui aceder às avaliações"
                )

            # Get reviews
            reviews = place_page.get_reviews(max_reviews=3)

            if not reviews:
                return IntentResponse(
                    success=True,
                    message="Este lugar ainda não tem avaliações"
                )

            # Format message with review count
            place_name = place_page.get_place_name() or "este lugar"
            message = f"A mostrar avaliações de {place_name}. "
            message += f"Encontrei {len(reviews)} avaliações recentes"

            return IntentResponse(
                success=True,
                message=message,
                data={"reviews": reviews}
            )

        except Exception as e:
            self.logger.error(f"Error showing reviews: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao obter as avaliações",
                data={"error": str(e)}
            )


@IntentRouter.register("show_photos")
class ShowPhotosHandler(BaseIntentHandler):
    """Handler for showing place photos."""

    supported_intents = ["show_photos"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Show photos for the current place.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            place_page = MapsPlacePage(context.driver)

            # Check if we're on a place page
            if not place_page.wait_for_place_details(timeout=5):
                return IntentResponse(
                    success=False,
                    message="Por favor seleciona um lugar primeiro para ver as fotos"
                )

            # Navigate to photos tab
            success = place_page.show_photos()
            if not success:
                return IntentResponse(
                    success=False,
                    message="Desculpa, não consegui aceder às fotos"
                )

            place_name = place_page.get_place_name() or "este lugar"
            return IntentResponse(
                success=True,
                message=f"A mostrar fotos de {place_name}"
            )

        except Exception as e:
            self.logger.error(f"Error showing photos: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao mostrar as fotos",
                data={"error": str(e)}
            )


@IntentRouter.register("get_opening_hours")
class GetOpeningHoursHandler(BaseIntentHandler):
    """Handler for getting opening hours."""

    supported_intents = ["get_opening_hours"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Get opening hours for the current place.

        Args:
            context: Intent context

        Returns:
            IntentResponse with opening hours
        """
        try:
            place_page = MapsPlacePage(context.driver)

            # Check if we're on a place page
            if not place_page.wait_for_place_details(timeout=5):
                return IntentResponse(
                    success=False,
                    message="Por favor seleciona um lugar primeiro para ver os horários"
                )

            # Get place name and open status
            place_name = place_page.get_place_name() or "Este lugar"
            is_open = place_page.is_open_now()

            if is_open is None:
                return IntentResponse(
                    success=True,
                    message=f"Informação de horários não está disponível para {place_name}"
                )

            status = "está aberto agora" if is_open else "está fechado agora"
            message = f"{place_name} {status}"

            return IntentResponse(
                success=True,
                message=message,
                data={"is_open": is_open}
            )

        except Exception as e:
            self.logger.error(f"Error getting opening hours: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao obter os horários",
                data={"error": str(e)}
            )


# General help and utility handlers

@IntentRouter.register("help")
class HelpHandler(BaseIntentHandler):
    """Handler for help requests."""

    supported_intents = ["help"]
    requires_confirmation = False
    confidence_threshold = 0.60

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Provide help information.

        Args:
            context: Intent context

        Returns:
            IntentResponse with help text
        """
        help_text = (
            "Posso ajudar-te com o Google Maps. "
            "Podes procurar lugares, obter direções, aproximar ou afastar, "
            "mudar a vista do mapa, mostrar trânsito, e obter informação de lugares como avaliações e fotos. "
            "Diz-me apenas o que queres fazer."
        )

        return IntentResponse(
            success=True,
            message=help_text
        )


@IntentRouter.register("cancel")
class CancelHandler(BaseIntentHandler):
    """Handler for cancel requests."""

    supported_intents = ["cancel"]
    requires_confirmation = False
    confidence_threshold = 0.60

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Cancel current operation.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        return IntentResponse(
            success=True,
            message="Cancelado"
        )
