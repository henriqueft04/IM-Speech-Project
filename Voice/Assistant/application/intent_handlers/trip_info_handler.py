"""
Intent handlers for trip information queries.
Handles questions about duration, distance, transport modes, route swapping, etc.
"""

import logging
import time
from typing import Optional

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter
from infrastructure.page_objects import MapsHomePage
from domain import TransportMode

logger = logging.getLogger(__name__)


@IntentRouter.register("get_trip_duration")
class GetTripDurationHandler(BaseIntentHandler):
    """Handler for asking 'quanto tempo demora?' (how long does it take?)"""

    supported_intents = ["get_trip_duration"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Get trip duration from Google Maps directions panel.

        Returns:
            IntentResponse with duration info
        """
        self.logger.info("Getting trip duration")

        try:
            home_page = MapsHomePage(context.driver)

            duration_xpaths = [
                "//div[contains(@class, 'section-directions-trip-duration')]//span",
                "//div[@id='section-directions-trip-0']//div[contains(@class, 'delay')]",
                "//div[contains(text(), 'min') or contains(text(), 'hora') or contains(text(), 'hour')]",
            ]

            duration_text = None
            for xpath in duration_xpaths:
                try:
                    element = context.driver.find_element("xpath", xpath)
                    if element.is_displayed():
                        duration_text = element.text
                        break
                except:
                    continue

            if not duration_text:
                return IntentResponse(
                    success=False,
                    message="Não consigo ver direções ativas. Pede direções primeiro."
                )

            return IntentResponse(
                success=True,
                message=f"A viagem demora {duration_text}",
                data={"duration": duration_text}
            )

        except Exception as e:
            self.logger.error(f"Error getting trip duration: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Desculpa, não consegui obter a duração da viagem"
            )


@IntentRouter.register("get_trip_distance")
class GetTripDistanceHandler(BaseIntentHandler):
    """Handler for asking 'quantos quilómetros?' (how many kilometers?)"""

    supported_intents = ["get_trip_distance"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Get trip distance from Google Maps directions panel.

        Returns:
            IntentResponse with distance info
        """
        self.logger.info("Getting trip distance")

        try:
            home_page = MapsHomePage(context.driver)

            distance_xpaths = [
                "//div[contains(@class, 'section-directions-trip-distance')]//span",
                "//div[@id='section-directions-trip-0']//div[contains(text(), 'km') or contains(text(), 'm')]",
            ]

            distance_text = None
            for xpath in distance_xpaths:
                try:
                    element = context.driver.find_element("xpath", xpath)
                    if element.is_displayed():
                        distance_text = element.text
                        break
                except:
                    continue

            if not distance_text:
                return IntentResponse(
                    success=False,
                    message="Não consigo ver direções ativas. Pede direções primeiro."
                )

            return IntentResponse(
                success=True,
                message=f"A distância é {distance_text}",
                data={"distance": distance_text}
            )

        except Exception as e:
            self.logger.error(f"Error getting trip distance: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Desculpa, não consegui obter a distância"
            )


@IntentRouter.register("change_transport_mode")
class ChangeTransportModeHandler(BaseIntentHandler):
    """Handler for changing transport mode (car, walking, transit, bike)"""

    supported_intents = ["change_transport_mode"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Change the transport mode for current directions.

        Returns:
            IntentResponse confirming mode change
        """
        transport_mode_str = context.get_entity("transport_mode")

        # Fallback to full text if no entity extracted
        if not transport_mode_str and context.metadata and "text" in context.metadata:
            full_text = context.metadata["text"].strip().lower()
            self.logger.info(f"No transport_mode entity, extracting from text: {full_text}")

            # Extract transport mode keywords from text
            keywords = {
                "caminhar": "caminhar",
                "andar": "andar",
                "pé": "a pé",
                "carro": "carro",
                "conduzir": "carro",
                "transportes": "transportes públicos",
                "autocarro": "transportes públicos",
                "comboio": "transportes públicos",
                "metro": "transportes públicos",
                "bicicleta": "bicicleta",
                "bike": "bicicleta",
                "mota": "mota",
                "scooter": "scooter",
            }

            for keyword, mode in keywords.items():
                if keyword in full_text:
                    transport_mode_str = mode
                    self.logger.info(f"Extracted '{mode}' from keyword '{keyword}'")
                    break

            if not transport_mode_str:
                transport_mode_str = full_text

        if not transport_mode_str:
            return IntentResponse(
                success=False,
                message="Que meio de transporte queres usar?"
            )

        self.logger.info(f"Changing transport mode to: {transport_mode_str}")

        try:
            transport_mode = TransportMode.from_string(transport_mode_str)

            home_page = MapsHomePage(context.driver)

            mode_map = {
                TransportMode.DRIVING: home_page.DRIVING_MODE,
                TransportMode.WALKING: home_page.WALKING_MODE,
                TransportMode.TRANSIT: home_page.TRANSIT_MODE,
                TransportMode.CYCLING: home_page.CYCLING_MODE,
            }

            locator = mode_map.get(transport_mode)
            if locator:
                home_page.select_transport_mode(locator)
                time.sleep(1)

                mode_names = {
                    TransportMode.DRIVING: "carro",
                    TransportMode.WALKING: "a pé",
                    TransportMode.TRANSIT: "transportes públicos",
                    TransportMode.CYCLING: "bicicleta",
                }

                return IntentResponse(
                    success=True,
                    message=f"Mudei para {mode_names[transport_mode]}",
                    data={"transport_mode": transport_mode.value}
                )
            else:
                return IntentResponse(
                    success=False,
                    message=f"Desculpa, não suporto o meio {transport_mode_str}"
                )

        except ValueError:
            return IntentResponse(
                success=False,
                message=f"Não reconheço o meio de transporte {transport_mode_str}"
            )
        except Exception as e:
            self.logger.error(f"Error changing transport mode: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Desculpa, não consegui mudar o meio de transporte"
            )


@IntentRouter.register("swap_route")
class SwapRouteHandler(BaseIntentHandler):
    """Handler for swapping origin and destination (inverter rota)"""

    supported_intents = ["swap_route", "reverse_route", "invert_route"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Swap the origin and destination of current route.

        Returns:
            IntentResponse confirming swap
        """
        self.logger.info("Swapping route origin and destination")

        try:
            home_page = MapsHomePage(context.driver)

            swap_button_xpaths = [
                "//button[@aria-label='Inverter ponto de partida e destino' or @aria-label='Reverse starting point and destination']",
                "//button[contains(@aria-label, 'Reverse') or contains(@aria-label, 'Inverter')]",
                "//button[@data-tooltip='Inverter origem e destino']",
            ]

            swapped = False
            for xpath in swap_button_xpaths:
                try:
                    swap_button = context.driver.find_element("xpath", xpath)
                    if swap_button.is_displayed():
                        swap_button.click()
                        swapped = True
                        self.logger.info("Clicked swap button")
                        break
                except:
                    continue

            if not swapped:
                return IntentResponse(
                    success=False,
                    message="Não consigo inverter a rota. Certifica-te que tens direções ativas."
                )

            time.sleep(1)

            return IntentResponse(
                success=True,
                message="Inverti a rota"
            )

        except Exception as e:
            self.logger.error(f"Error swapping route: {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message="Desculpa, não consegui inverter a rota"
            )
