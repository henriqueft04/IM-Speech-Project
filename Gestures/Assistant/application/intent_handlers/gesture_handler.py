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
    """Handler for swipe left gesture - pan map left or rotate camera left in street view."""

    supported_intents = ["gesture_swipe_left"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe left gesture.
        - In Street View: rotate camera left
        - On map: pan map to show what's on the left
        """
        try:
            home_page = MapsHomePage(context.driver)

            if home_page._is_in_street_view():
                # Street View: rotate camera left
                success = home_page.rotate_street_view("left")
                return IntentResponse(
                    success=success,
                    message="A olhar para a esquerda" if success else "Não consegui rodar"
                )
            else:
                # Map view: pan left
                success = home_page.pan_map("left", times=3)
                return IntentResponse(
                    success=success,
                    message="A mover para a esquerda" if success else "Não consegui mover o mapa"
                )

        except Exception as e:
            self.logger.error(f"Error handling swipe left: {e}", exc_info=True)
            return IntentResponse(success=False, message="Ocorreu um erro", data={"error": str(e)})


@IntentRouter.register("gesture_swipe_right")
class SwipeRightHandler(BaseIntentHandler):
    """Handler for swipe right gesture - pan map right or rotate camera right in street view."""

    supported_intents = ["gesture_swipe_right"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe right gesture.
        - In Street View: rotate camera right
        - On map: pan map to show what's on the right
        """
        try:
            home_page = MapsHomePage(context.driver)

            if home_page._is_in_street_view():
                # Street View: rotate camera right
                success = home_page.rotate_street_view("right")
                return IntentResponse(
                    success=success,
                    message="A olhar para a direita" if success else "Não consegui rodar"
                )
            else:
                # Map view: pan right
                success = home_page.pan_map("right", times=3)
                return IntentResponse(
                    success=success,
                    message="A mover para a direita" if success else "Não consegui mover o mapa"
                )

        except Exception as e:
            self.logger.error(f"Error handling swipe right: {e}", exc_info=True)
            return IntentResponse(success=False, message="Ocorreu um erro", data={"error": str(e)})


@IntentRouter.register("gesture_swipe_up")
class SwipeUpHandler(BaseIntentHandler):
    """Handler for swipe up gesture - pan map up or move forward in street view."""

    supported_intents = ["gesture_swipe_up"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe up gesture.
        - In Street View: move forward
        - On map: pan map to show what's above
        """
        try:
            home_page = MapsHomePage(context.driver)

            if home_page._is_in_street_view():
                # Street View: move forward
                success = home_page.move_forward_street_view()
                return IntentResponse(
                    success=success,
                    message="A avançar" if success else "Não consegui avançar"
                )
            else:
                # Map view: pan up
                success = home_page.pan_map("up", times=3)
                return IntentResponse(
                    success=success,
                    message="A mover para cima" if success else "Não consegui mover o mapa"
                )

        except Exception as e:
            self.logger.error(f"Error handling swipe up: {e}", exc_info=True)
            return IntentResponse(success=False, message="Ocorreu um erro", data={"error": str(e)})


@IntentRouter.register("gesture_swipe_down")
class SwipeDownHandler(BaseIntentHandler):
    """Handler for swipe down gesture - pan map down or move backward in street view."""

    supported_intents = ["gesture_swipe_down"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle swipe down gesture.
        - In Street View: move backward
        - On map: pan map to show what's below
        """
        try:
            home_page = MapsHomePage(context.driver)

            if home_page._is_in_street_view():
                # Street View: move backward
                success = home_page.move_backward_street_view()
                return IntentResponse(
                    success=success,
                    message="A recuar" if success else "Não consegui recuar"
                )
            else:
                # Map view: pan down
                success = home_page.pan_map("down", times=3)
                return IntentResponse(
                    success=success,
                    message="A mover para baixo" if success else "Não consegui mover o mapa"
                )

        except Exception as e:
            self.logger.error(f"Error handling swipe down: {e}", exc_info=True)
            return IntentResponse(success=False, message="Ocorreu um erro", data={"error": str(e)})



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


@IntentRouter.register("gesture_transports")
class TransportsFilterHandler(BaseIntentHandler):
    """Handler for selecting transit/transports filter via gesture."""

    supported_intents = ["gesture_transports"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Select the transit/transport filter on Google Maps.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)
            home_page.click_filter_button("Transportes públicos")

            return IntentResponse(
                success=True,
                message="A mostrar transportes públicos na área"
            )

        except Exception as e:
            self.logger.error(f"Error selecting transports filter: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao selecionar transportes",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_camera")
class CameraHandler(BaseIntentHandler):
    """Handler for camera gesture - open 'Coisas a fazer' (Explore/Activities)."""

    supported_intents = ["gesture_camera"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle camera gesture - open 'Coisas a fazer' menu.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            if home_page.open_explore_menu():
                return IntentResponse(
                    success=True,
                    message="A abrir coisas a fazer"
                )
            else:
                return IntentResponse(
                    success=False,
                    message="Não encontrei o botão 'Coisas a fazer'"
                )

        except Exception as e:
            self.logger.error(f"Error opening explore menu: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_enter_street")
class EnterStreetHandler(BaseIntentHandler):
    """Handler for entering street view via gesture."""

    supported_intents = ["gesture_enter_street"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Enter street view mode.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            if home_page.enter_street_view():
                return IntentResponse(
                    success=True,
                    message="A entrar em vista de rua"
                )
            else:
                return IntentResponse(
                    success=False,
                    message="Não foi possível entrar em vista de rua nesta localização"
                )

        except Exception as e:
            self.logger.error(f"Error entering street view: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao entrar em vista de rua",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_exit_street")
class ExitStreetHandler(BaseIntentHandler):
    """Handler for exiting street view via gesture."""

    supported_intents = ["gesture_exit_street"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Exit street view mode.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            home_page = MapsHomePage(context.driver)

            if home_page.exit_street_view():
                return IntentResponse(
                    success=True,
                    message="A sair de vista de rua"
                )
            else:
                return IntentResponse(
                    success=False,
                    message="Não foi possível sair de vista de rua"
                )

        except Exception as e:
            self.logger.error(f"Error exiting street view: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao sair de vista de rua",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_forward")
class ForwardHandler(BaseIntentHandler):
    """Handler for forward gesture in street view - move forward."""

    supported_intents = ["gesture_forward"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Move forward in street view.

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
                    message="Não estou em vista de rua"
                )

            # Try to move forward
            success = home_page.move_forward_street_view()

            if success:
                return IntentResponse(
                    success=True,
                    message="A avançar"
                )
            else:
                return IntentResponse(
                    success=False,
                    message="Não consegui avançar"
                )

        except Exception as e:
            self.logger.error(f"Error moving forward: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_select")
class SelectHandler(BaseIntentHandler):
    """Handler for select gesture - click on current item."""

    supported_intents = ["gesture_select"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Select/click the current focused item.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            from infrastructure.page_objects import MapsSearchResultsPage

            # Try to select the first search result if available
            results_page = MapsSearchResultsPage(context.driver)
            results_page.select_result_by_index(0)

            return IntentResponse(
                success=True,
                message="Selecionado"
            )

        except Exception as e:
            self.logger.error(f"Error selecting: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro ao selecionar",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_up_option")
class UpOptionHandler(BaseIntentHandler):
    """Handler for up option gesture - navigate up in list."""

    supported_intents = ["gesture_up_option"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Navigate up in search results or menu options.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            from selenium.webdriver.common.keys import Keys
            # Press Arrow Up to navigate
            context.driver.find_element("tag name", "body").send_keys(Keys.ARROW_UP)

            return IntentResponse(
                success=True,
                message="Opção anterior"
            )

        except Exception as e:
            self.logger.error(f"Error navigating up: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )


@IntentRouter.register("gesture_down_option")
class DownOptionHandler(BaseIntentHandler):
    """Handler for down option gesture - navigate down in list."""

    supported_intents = ["gesture_down_option"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Navigate down in search results or menu options.

        Args:
            context: Intent context

        Returns:
            IntentResponse
        """
        try:
            from selenium.webdriver.common.keys import Keys
            # Press Arrow Down to navigate
            context.driver.find_element("tag name", "body").send_keys(Keys.ARROW_DOWN)

            return IntentResponse(
                success=True,
                message="Próxima opção"
            )

        except Exception as e:
            self.logger.error(f"Error navigating down: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Ocorreu um erro",
                data={"error": str(e)}
            )
