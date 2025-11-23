"""
Google Maps Voice Assistant Orchestrator.
Main class that coordinates all components.
"""

import logging
from typing import Dict, Any, Optional

from selenium.webdriver.remote.webdriver import WebDriver

from application.intent_handlers import IntentContext, IntentResponse
from application.services import IntentRouter, ConfirmationService, TTSService
from config.settings import HIGH_CONFIDENCE_THRESHOLD
from domain import MapState

logger = logging.getLogger(__name__)


class GoogleMapsAssistant:
    """
    Main orchestrator for the Google Maps voice assistant.

    Coordinates:
    - Intent routing
    - Confirmation flow
    - TTS feedback
    - State management
    """

    def __init__(
        self,
        driver: WebDriver,
        tts_service: Optional[TTSService] = None
    ):
        """
        Initialize the assistant.

        Args:
            driver: Selenium WebDriver instance
            tts_service: TTS service for voice feedback (optional)
        """
        self.driver = driver
        self.tts_service = tts_service or TTSService()
        self.confirmation_service = ConfirmationService()
        self.map_state = MapState()

        logger.info("Google Maps Assistant initialized")

    def handle_intent(
        self,
        intent: str,
        confidence: float,
        entities: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Handle an intent from NLU.

        Args:
            intent: Intent name
            confidence: NLU confidence score (0-1)
            entities: Extracted entities
            metadata: Additional metadata

        Returns:
            Response message for TTS
        """
        logger.info(
            f"Handling intent: {intent}, confidence: {confidence:.2f}, "
            f"entities: {entities}"
        )

        # Check for affirmation/denial of pending confirmation
        if self.confirmation_service.has_pending_confirmation():
            if intent == "affirm":
                return self._handle_affirmation()
            elif intent == "deny":
                return self._handle_denial()

        # Create intent context
        context = IntentContext(
            intent=intent,
            confidence=confidence,
            entities=entities,
            driver=self.driver,
            metadata=metadata
        )

        # Route intent to handler
        response = IntentRouter.handle_intent(context)

        # Check if confirmation is needed
        if response.requires_follow_up:
            return self._handle_confirmation_required(
                intent, confidence, entities, response
            )

        # Update map state if relevant
        self._update_map_state(intent, entities, response)

        # Return feedback message
        return response.message

    def _handle_confirmation_required(
        self,
        intent: str,
        confidence: float,
        entities: Dict[str, Any],
        response: IntentResponse
    ) -> str:
        """
        Handle when confirmation is required.

        Args:
            intent: Intent name
            confidence: Confidence score
            entities: Entities
            response: Handler response

        Returns:
            Confirmation message
        """
        # Store pending confirmation
        self.confirmation_service.set_pending_confirmation(
            intent=intent,
            confidence=confidence,
            entities=entities,
            context=response.follow_up_data
        )

        # Generate confirmation message
        confirmation_msg = self.confirmation_service.generate_confirmation_message(
            intent, entities
        )

        logger.info(f"Requesting confirmation: {confirmation_msg}")
        return confirmation_msg

    def _handle_affirmation(self) -> str:
        """
        Handle affirmative response to confirmation.

        Returns:
            Response message
        """
        logger.info("Handling affirmation")

        confirmation = self.confirmation_service.process_affirmation()

        if not confirmation:
            return "Não tenho a certeza do que estás a confirmar. Podes repetir o teu pedido?"

        # Re-execute the intent with high confidence
        return self.handle_intent(
            intent=confirmation.intent,
            confidence=1.0,  # Override with high confidence
            entities=confirmation.entities,
            metadata=confirmation.context
        )

    def _handle_denial(self) -> str:
        """
        Handle negative response to confirmation.

        Returns:
            Response message
        """
        logger.info("Handling denial")

        was_denied = self.confirmation_service.process_denial()

        if not was_denied:
            return "Está bem"

        return "Cancelado. O que queres fazer em vez disso?"

    def _update_map_state(
        self,
        intent: str,
        entities: Dict[str, Any],
        response: IntentResponse
    ):
        """
        Update map state based on successful intent execution.

        Args:
            intent: Intent name
            entities: Entities
            response: Handler response
        """
        if not response.success:
            return

        try:
            # Update state based on intent
            if intent == "search_location":
                self.map_state.last_search_query = entities.get("location")
                if response.data and "search_results" in response.data:
                    self.map_state.search_results = response.data["search_results"].locations

            elif intent == "change_map_type":
                from domain import MapType
                map_type_str = entities.get("map_type")
                if map_type_str:
                    try:
                        self.map_state.map_type = MapType.from_string(map_type_str)
                    except ValueError:
                        pass

            elif intent == "show_traffic":
                self.map_state.traffic_enabled = True

            elif intent == "hide_traffic":
                self.map_state.traffic_enabled = False

            elif intent == "show_place_details":
                if response.data and "place_details" in response.data:
                    self.map_state.selected_place = response.data["place_details"]

            # Update timestamp
            self.map_state.update_timestamp()

        except Exception as e:
            logger.warning(f"Failed to update map state: {e}")

    def get_map_state(self) -> MapState:
        """
        Get current map state.

        Returns:
            MapState object
        """
        return self.map_state

    def reset_state(self):
        """Reset the assistant state."""
        self.map_state = MapState()
        self.confirmation_service.clear_pending_confirmation()
        logger.info("Assistant state reset")

    async def speak(self, message: str, priority: str = "normal"):
        """
        Send a message to TTS service.

        Args:
            message: Message to speak
            priority: Priority level
        """
        await self.tts_service.speak(message, priority)

    def set_tts_websocket(self, websocket):
        """
        Set WebSocket connection for TTS service.

        Args:
            websocket: WebSocket connection
        """
        self.tts_service.set_websocket(websocket)
        logger.info("TTS WebSocket connection set")

    def shutdown(self):
        """Gracefully shutdown the assistant."""
        logger.info("Shutting down Google Maps Assistant")
        self.reset_state()

    def __str__(self) -> str:
        """String representation."""
        return (
            f"GoogleMapsAssistant("
            f"handlers={len(IntentRouter._handlers)}, "
            f"state={self.map_state}"
            f")"
        )
