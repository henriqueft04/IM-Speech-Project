"""
Base intent handler class.
All specific intent handlers should inherit from this class.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


@dataclass
class IntentContext:
    """
    Context passed to intent handlers containing all necessary data.

    Attributes:
        intent: Intent name from NLU
        confidence: NLU confidence score (0-1)
        entities: Dictionary of extracted entities
        driver: Selenium WebDriver instance
        metadata: Additional metadata (user_id, session_id, etc.)
    """
    intent: str
    confidence: float
    entities: Dict[str, Any]
    driver: WebDriver
    metadata: Optional[Dict[str, Any]] = None

    def get_entity(self, key: str, default: Any = None) -> Any:
        """Get entity value with optional default."""
        return self.entities.get(key, default)


@dataclass
class IntentResponse:
    """
    Response from intent handler execution.

    Attributes:
        success: Whether the intent was executed successfully
        message: Human-readable feedback message for TTS
        data: Additional data (e.g., search results, place info)
        requires_follow_up: Whether a follow-up action is needed
        follow_up_data: Data for follow-up action
    """
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    requires_follow_up: bool = False
    follow_up_data: Optional[Dict[str, Any]] = None


class BaseIntentHandler(ABC):
    """
    Abstract base class for all intent handlers.

    Subclasses must implement the execute() method and define
    configuration properties.
    """

    # Configuration - override in subclasses
    requires_confirmation: bool = False
    confidence_threshold: float = 0.75
    supported_intents: list = []

    def __init__(self):
        """Initialize the handler."""
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Execute the intent handler logic.

        Args:
            context: Intent context with driver, entities, etc.

        Returns:
            IntentResponse with result and feedback

        Raises:
            Exception: If execution fails
        """
        pass

    def validate_entities(
        self,
        context: IntentContext,
        required_entities: list
    ) -> tuple[bool, Optional[str]]:
        """
        Validate that required entities are present.

        Args:
            context: Intent context
            required_entities: List of required entity keys

        Returns:
            Tuple of (is_valid, error_message)
        """
        missing = [
            entity for entity in required_entities
            if entity not in context.entities or not context.entities[entity]
        ]

        if missing:
            error_msg = f"Missing required entities: {', '.join(missing)}"
            self.logger.warning(error_msg)
            return False, error_msg

        return True, None

    def can_handle(self, intent: str) -> bool:
        """
        Check if this handler can handle the given intent.

        Args:
            intent: Intent name

        Returns:
            True if handler supports this intent
        """
        return intent in self.supported_intents

    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(intents={self.supported_intents})"
