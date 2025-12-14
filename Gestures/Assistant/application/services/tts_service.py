"""
Text-to-Speech service for providing voice feedback.
Sends directly to browser via WebSocket on port 8083 (bypasses FusionEngine).
"""

import logging
import websockets
import json

logger = logging.getLogger(__name__)


class TTSService:
    """
    Service for handling text-to-speech feedback.

    Sends JSON messages directly to browser via WebSocket.
    """

    def __init__(self, websocket=None):
        """
        Initialize TTS service.

        Args:
            websocket: WebSocket connection (not used, kept for compatibility)
        """
        self.websocket = websocket
        self.tts_ws_url = "ws://127.0.0.1:8083"

    async def speak(self, message: str, language: str = "pt-PT"):
        """
        Send a message for TTS synthesis directly to browser WebSocket.

        Args:
            message: Text to speak
            language: Language code (default: pt-PT)
        """
        if not message:
            logger.warning("Empty message provided to TTS")
            return

        logger.info(f"TTS: {message}")

        try:
            # Create simple JSON message
            tts_data = json.dumps({
                "text": message,
                "language": language
            })

            # Send directly to browser via WebSocket (bypasses FusionEngine)
            async with websockets.connect(self.tts_ws_url) as ws:
                await ws.send(tts_data)
                logger.info(f"Sent TTS message to browser: {message}")

        except Exception as e:
            logger.error(f"Failed to send TTS message: {e}", exc_info=True)

    def speak_sync(self, message: str, language: str = "pt-PT"):
        """
        Synchronous version of speak (for non-async contexts).

        Args:
            message: Text to speak
            language: Language code
        """
        if not message:
            logger.warning("Empty message provided to TTS")
            return

        logger.info(f"TTS: {message}")
        # In a real implementation, this would queue the message
        # or use a synchronous sending mechanism

    def set_websocket(self, websocket):
        """
        Set or update the WebSocket connection.

        Args:
            websocket: WebSocket connection
        """
        self.websocket = websocket
        logger.info("WebSocket connection set for TTS service")


class FeedbackMessages:
    """Predefined feedback messages for common scenarios - pt-PT."""

    # Success messages
    SUCCESS_SEARCH = "Encontrei {count} resultado{plural}"
    SUCCESS_DIRECTIONS = "A mostrar direções para {destination}"
    SUCCESS_NAVIGATION_START = "Navegação iniciada"
    SUCCESS_ZOOM_IN = "Aproximado"
    SUCCESS_ZOOM_OUT = "Afastado"
    SUCCESS_MAP_TYPE_CHANGED = "Vista alterada para {map_type}"
    SUCCESS_TRAFFIC_SHOWN = "A mostrar trânsito"
    SUCCESS_TRAFFIC_HIDDEN = "Trânsito escondido"

    # Error messages
    ERROR_NO_RESULTS = "Não consegui encontrar resultados para {query}"
    ERROR_SEARCH_FAILED = "Desculpa, não consegui procurar {query}"
    ERROR_DIRECTIONS_FAILED = "Desculpa, não consegui obter direções para {destination}"
    ERROR_GENERIC = "Ocorreu um erro ao processar o teu pedido"
    ERROR_NOT_UNDERSTOOD = "Não percebi. Podes repetir?"
    ERROR_NO_LOCATION = "Não percebi a localização. Que lugar procuras?"

    # Confirmation messages
    CONFIRM_SEARCH = "Querias procurar {location}?"
    CONFIRM_DIRECTIONS = "Devo obter direções para {destination}?"
    CONFIRM_NAVIGATION = "Devo iniciar a navegação?"

    # Info messages
    INFO_PLACE_OPEN = "{place} está aberto agora"
    INFO_PLACE_CLOSED = "{place} está fechado agora"
    INFO_RATING = "{place} tem {rating} estrelas com {count} avaliações"

    @staticmethod
    def format(template: str, **kwargs) -> str:
        """
        Format a message template with provided values.

        Args:
            template: Message template
            **kwargs: Values to substitute

        Returns:
            Formatted message
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            logger.warning(f"Missing template key: {e}")
            return template

    @staticmethod
    def pluralize(count: int, singular: str = "", plural: str = "s") -> str:
        """
        Get plural suffix based on count.

        Args:
            count: Number to check
            singular: Singular form (default: empty string)
            plural: Plural form (default: "s")

        Returns:
            Appropriate form based on count
        """
        return singular if count == 1 else plural
