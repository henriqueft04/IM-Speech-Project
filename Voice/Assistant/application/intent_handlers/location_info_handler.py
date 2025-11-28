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


@IntentRouter.register("get_location_info")
class GetLocationInfoHandler(BaseIntentHandler):
    """Handler for getting general location information."""

    supported_intents = ["get_location_info"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Get information about the current location.

        Args:
            context: Intent context

        Returns:
            IntentResponse with location info
        """
        try:
            place_page = MapsPlacePage(context.driver)

            # Try to get place details - don't fail if page isn't fully loaded
            place_page.wait_for_place_details(timeout=3)

            # Get place details - individual methods handle missing elements gracefully
            place_name = place_page.get_place_name()
            address = place_page.get_address()
            rating = place_page.get_rating()
            review_count = place_page.get_total_ratings()

            # Build message
            message_parts = []
            if place_name:
                message_parts.append(place_name)
            if address:
                message_parts.append(address)
            if rating:
                message_parts.append(f"Classificação {rating} estrelas")
            if review_count:
                message_parts.append(f"{review_count} avaliações")

            # If we got no information at all, the place isn't selected
            if not message_parts:
                return IntentResponse(
                    success=False,
                    message="Por favor seleciona um lugar primeiro"
                )

            message = ". ".join(message_parts)

            return IntentResponse(
                success=True,
                message=message,
                data={
                    "place_name": place_name,
                    "address": address,
                    "rating": rating,
                    "review_count": review_count
                }
            )

        except Exception as e:
            self.logger.error(f"Error getting location info: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao obter informações do lugar",
                data={"error": str(e)}
            )


@IntentRouter.register("whats_here")
class WhatsHereHandler(BaseIntentHandler):
    """Handler for identifying what's at a map location."""

    supported_intents = ["whats_here"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Identify what's at the current map location using right-click.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.common.by import By
            import time

            # Find the map canvas
            map_canvas = context.driver.find_element(By.ID, "map")

            # Right-click the center of the map
            actions = ActionChains(context.driver)
            actions.context_click(map_canvas).perform()
            time.sleep(0.5)

            # Click "What's here?" option
            whats_here_xpath = "//div[contains(text(), \"What's here\") or contains(text(), 'O que há aqui')]"
            whats_here_button = context.driver.find_element(By.XPATH, whats_here_xpath)
            whats_here_button.click()

            time.sleep(1)

            # Wait for location info to load
            place_page = MapsPlacePage(context.driver)
            if place_page.wait_for_place_details(timeout=5):
                place_name = place_page.get_place_name()
                if place_name:
                    return IntentResponse(
                        success=True,
                        message=f"Isto é {place_name}",
                        data={"place_name": place_name}
                    )

            # If no place name found, try to get coordinates
            return IntentResponse(
                success=True,
                message="A mostrar informação sobre este local"
            )

        except Exception as e:
            self.logger.error(f"Error identifying location: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Não consegui identificar este local",
                data={"error": str(e)}
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
