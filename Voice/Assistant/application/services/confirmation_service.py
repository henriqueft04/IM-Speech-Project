"""
Confirmation service for handling action-specific confirmations.
"""

import logging
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass

from config.settings import REQUIRES_CONFIRMATION, MEDIUM_CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)


@dataclass
class PendingConfirmation:
    """
    Represents a pending confirmation for a low-confidence intent.

    Attributes:
        intent: Original intent name
        confidence: Original confidence score
        entities: Original entities
        handler: Handler function to call if confirmed
        context: Additional context data
    """
    intent: str
    confidence: float
    entities: Dict[str, Any]
    handler: Optional[Callable] = None
    context: Optional[Dict[str, Any]] = None


class ConfirmationService:
    """
    Service for managing action confirmations.

    Handles:
    - Determining if an intent requires confirmation
    - Storing pending confirmations
    - Processing affirmative/negative responses
    """

    def __init__(self):
        """Initialize the confirmation service."""
        self._pending_confirmation: Optional[PendingConfirmation] = None

    def requires_confirmation(
        self,
        intent: str,
        confidence: float,
        handler_requires_confirmation: bool = False
    ) -> bool:
        """
        Determine if an intent requires user confirmation.

        Args:
            intent: Intent name
            confidence: NLU confidence score (0-1)
            handler_requires_confirmation: Whether the handler explicitly requires confirmation

        Returns:
            True if confirmation is needed
        """
        if handler_requires_confirmation:
            logger.info(f"Intent '{intent}' requires confirmation (handler requirement)")
            return True

        # Check action-specific configuration
        if REQUIRES_CONFIRMATION.get(intent, False):
            logger.info(f"Intent '{intent}' requires confirmation (config requirement)")
            return True

        # Check confidence threshold
        if confidence < MEDIUM_CONFIDENCE_THRESHOLD:
            logger.info(
                f"Intent '{intent}' requires confirmation "
                f"(low confidence: {confidence:.2f})"
            )
            return True

        return False

    def set_pending_confirmation(
        self,
        intent: str,
        confidence: float,
        entities: Dict[str, Any],
        handler: Optional[Callable] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Store a pending confirmation.

        Args:
            intent: Intent name
            confidence: Confidence score
            entities: Extracted entities
            handler: Handler to call if confirmed
            context: Additional context
        """
        self._pending_confirmation = PendingConfirmation(
            intent=intent,
            confidence=confidence,
            entities=entities,
            handler=handler,
            context=context
        )
        logger.info(f"Set pending confirmation for intent '{intent}'")

    def get_pending_confirmation(self) -> Optional[PendingConfirmation]:
        """
        Get the current pending confirmation.

        Returns:
            PendingConfirmation or None
        """
        return self._pending_confirmation

    def clear_pending_confirmation(self):
        """Clear the pending confirmation."""
        if self._pending_confirmation:
            logger.info(
                f"Cleared pending confirmation for intent '{self._pending_confirmation.intent}'"
            )
        self._pending_confirmation = None

    def has_pending_confirmation(self) -> bool:
        """
        Check if there's a pending confirmation.

        Returns:
            True if confirmation is pending
        """
        return self._pending_confirmation is not None

    def generate_confirmation_message(
        self,
        intent: str,
        entities: Dict[str, Any]
    ) -> str:
        """
        Generate a contextual confirmation message.

        Args:
            intent: Intent name
            entities: Extracted entities

        Returns:
            Confirmation question for TTS
        """
        confirmation_templates = {
            "search_location": "Querias procurar {location}?",
            "get_directions": "Devo obter direções para {destination}?",
            "start_navigation": "Devo iniciar a navegação?",
            "show_place_details": "Querias ver os detalhes do lugar?",
            "show_reviews": "Devo mostrar as avaliações?",
            "show_photos": "Querias ver as fotos?",
            "zoom_in": "Querias aumentar o zoom?",
            "zoom_out": "Querias diminuir o zoom?",
            "recenter_map": "Querias recentrar o mapa?",
            "center_location": "Querias centrar o mapa em {location}?",
            "clear_map": "Querias limpar o mapa?",
            "toggle_satellite": "Querias mudar para vista de satélite?",
            "show_traffic": "Querias mostrar o trânsito?",
            "hide_traffic": "Querias esconder o trânsito?",
            "get_trip_duration": "Querias saber quanto tempo demora?",
            "get_trip_distance": "Querias saber a distância?",
            "change_transport_mode": "Querias mudar o meio de transporte?",
            "swap_route": "Querias inverter a rota?",
            "select_place": "Querias selecionar este lugar?",
            "select_alternative_route": "Querias usar uma rota alternativa?",
            "get_location_info": "Querias informações sobre este lugar?",
            "whats_here": "Querias saber o que está aqui?",
            "stop_navigation": "Querias parar a navegação?",
            "change_map_type": "Querias mudar o tipo de mapa?",
            "get_opening_hours": "Querias saber os horários?",
            "goodbye": "Querias desligar?",
            "cancel": "Querias cancelar?",
            "greet": "Olá! Como posso ajudar?",
            "thank_you": "De nada!",
            "help": "Querias ajuda?",
        }

        template = confirmation_templates.get(
            intent,
            f"Querias {intent.replace('_', ' ')}?"
        )

        try:
            if intent == "center_location" and "destination" in entities and "location" not in entities:
                entities["location"] = entities["destination"]

            return template.format(**entities)
        except KeyError:
            return template

    def process_affirmation(self) -> Optional[PendingConfirmation]:
        """
        Process affirmative response (yes).

        Returns:
            The pending confirmation to execute, or None
        """
        if not self.has_pending_confirmation():
            logger.warning("No pending confirmation to affirm")
            return None

        confirmation = self._pending_confirmation
        logger.info(f"User affirmed intent '{confirmation.intent}'")

        self.clear_pending_confirmation()

        return confirmation

    def process_denial(self) -> bool:
        """
        Process negative response (no).

        Returns:
            True if there was a confirmation to deny
        """
        if not self.has_pending_confirmation():
            logger.warning("No pending confirmation to deny")
            return False

        intent = self._pending_confirmation.intent
        logger.info(f"User denied intent '{intent}'")

        self.clear_pending_confirmation()

        return True
