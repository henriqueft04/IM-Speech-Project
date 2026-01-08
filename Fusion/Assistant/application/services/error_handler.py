"""
Centralized error handling and user-friendly error messages.
Converts technical exceptions into clear Portuguese messages for TTS.
"""

import logging
from typing import Optional, Tuple
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException
)

logger = logging.getLogger(__name__)


class ErrorCategory:
    """Error category constants"""
    NETWORK = "network"
    BROWSER = "browser"
    ELEMENT_NOT_FOUND = "element_not_found"
    TIMEOUT = "timeout"
    INTERACTION = "interaction"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


class ErrorHandler:
    """
    Central error handler that converts exceptions to user-friendly messages.
    All messages are in Portuguese (pt-PT) for TTS output.
    """

    # Map of error categories to user-friendly messages
    ERROR_MESSAGES = {
        ErrorCategory.NETWORK: "Não consigo aceder ao Google Maps. Verifica a tua ligação à Internet.",
        ErrorCategory.BROWSER: "O browser encontrou um problema. Vou tentar outra vez.",
        ErrorCategory.ELEMENT_NOT_FOUND: "Não encontrei o elemento no mapa. O Google Maps pode ter mudado.",
        ErrorCategory.TIMEOUT: "A operação demorou muito tempo. Tenta outra vez.",
        ErrorCategory.INTERACTION: "Não consegui interagir com o mapa. Tenta outra vez.",
        ErrorCategory.VALIDATION: "Os dados fornecidos não são válidos.",
        ErrorCategory.UNKNOWN: "Ocorreu um erro inesperado. Tenta outra vez."
    }

    # Specific error messages for common scenarios
    SPECIFIC_MESSAGES = {
        "no_results": "Não encontrei resultados para a tua pesquisa.",
        "missing_destination": "Para onde queres ir? Não percebi o destino.",
        "missing_location": "Que lugar queres procurar? Não percebi a localização.",
        "invalid_transport_mode": "Esse modo de transporte não é válido. Usa carro, a pé, transportes públicos, ou bicicleta.",
        "no_directions": "Preciso que primeiro obtenhas direções antes de iniciar a navegação.",
        "place_not_found": "Não encontrei esse lugar. Tenta ser mais específico.",
        "search_failed": "Não consegui fazer a pesquisa. Tenta outra vez.",
        "directions_failed": "Não consegui obter direções. Verifica o destino e tenta outra vez.",
        "navigation_failed": "Não consegui iniciar a navegação. Certifica-te que tens direções definidas.",
        "map_type_failed": "Não consegui mudar o tipo de mapa.",
        "zoom_failed": "Não consegui fazer zoom no mapa.",
        "traffic_failed": "Não consegui mostrar o tráfego.",
    }

    @classmethod
    def handle_exception(
        cls,
        exception: Exception,
        context: str = "",
        fallback_message: Optional[str] = None
    ) -> Tuple[str, ErrorCategory]:
        """
        Convert exception to user-friendly Portuguese message.

        Args:
            exception: The exception to handle
            context: Context string for logging (e.g., "searching for location")
            fallback_message: Optional custom fallback message

        Returns:
            Tuple of (user_message, error_category)
        """
        # Log the full exception with context
        log_message = f"Error {context}: {type(exception).__name__}: {str(exception)}"
        logger.error(log_message, exc_info=True)

        # Determine category and message based on exception type
        category, message = cls._categorize_exception(exception)

        # Use fallback message if provided
        if fallback_message:
            message = fallback_message

        # Log what we're telling the user
        logger.info(f"User message: {message} (category: {category})")

        return message, category

    @classmethod
    def _categorize_exception(cls, exception: Exception) -> Tuple[ErrorCategory, str]:
        """
        Categorize exception and get appropriate message.

        Args:
            exception: The exception to categorize

        Returns:
            Tuple of (category, user_message)
        """
        # Selenium-specific exceptions
        if isinstance(exception, NoSuchElementException):
            return ErrorCategory.ELEMENT_NOT_FOUND, cls.ERROR_MESSAGES[ErrorCategory.ELEMENT_NOT_FOUND]

        elif isinstance(exception, TimeoutException):
            return ErrorCategory.TIMEOUT, cls.ERROR_MESSAGES[ErrorCategory.TIMEOUT]

        elif isinstance(exception, StaleElementReferenceException):
            return ErrorCategory.ELEMENT_NOT_FOUND, "O elemento mudou. Vou tentar outra vez."

        elif isinstance(exception, (ElementNotInteractableException, ElementClickInterceptedException)):
            return ErrorCategory.INTERACTION, cls.ERROR_MESSAGES[ErrorCategory.INTERACTION]

        elif isinstance(exception, WebDriverException):
            # Check if it's a network/connection issue
            error_msg = str(exception).lower()
            if any(keyword in error_msg for keyword in ["connection", "network", "dns", "timeout"]):
                return ErrorCategory.NETWORK, cls.ERROR_MESSAGES[ErrorCategory.NETWORK]
            else:
                return ErrorCategory.BROWSER, cls.ERROR_MESSAGES[ErrorCategory.BROWSER]

        # Validation errors
        elif isinstance(exception, (ValueError, KeyError, TypeError)):
            return ErrorCategory.VALIDATION, cls.ERROR_MESSAGES[ErrorCategory.VALIDATION]

        # Unknown exception
        else:
            return ErrorCategory.UNKNOWN, cls.ERROR_MESSAGES[ErrorCategory.UNKNOWN]

    @classmethod
    def get_specific_message(cls, key: str, **kwargs) -> str:
        """
        Get a specific error message by key, with optional formatting.

        Args:
            key: Message key from SPECIFIC_MESSAGES
            **kwargs: Values to format into the message

        Returns:
            Formatted error message

        Example:
            >>> ErrorHandler.get_specific_message("missing_destination")
            "Para onde queres ir? Não percebi o destino."
        """
        message = cls.SPECIFIC_MESSAGES.get(key, cls.ERROR_MESSAGES[ErrorCategory.UNKNOWN])

        # Format message if kwargs provided
        try:
            return message.format(**kwargs)
        except KeyError as e:
            logger.warning(f"Missing format key in error message: {e}")
            return message

    @classmethod
    def format_exception_for_user(cls, exception: Exception) -> str:
        """
        Quick method to get just the user message from an exception.

        Args:
            exception: The exception to format

        Returns:
            User-friendly message in Portuguese
        """
        message, _ = cls.handle_exception(exception)
        return message


class ValidationError(Exception):
    """Custom exception for validation errors with user-friendly messages."""

    def __init__(self, user_message: str, technical_details: str = ""):
        """
        Initialize validation error.

        Args:
            user_message: User-friendly message in Portuguese
            technical_details: Technical details for logging
        """
        self.user_message = user_message
        self.technical_details = technical_details
        super().__init__(technical_details or user_message)

    def __str__(self):
        return self.user_message


class OperationFailedError(Exception):
    """Custom exception for failed operations with context."""

    def __init__(self, operation: str, reason: str = ""):
        """
        Initialize operation failed error.

        Args:
            operation: Name of the operation that failed
            reason: Reason for failure
        """
        self.operation = operation
        self.reason = reason
        super().__init__(f"{operation} failed: {reason}")


# Convenience functions for common error scenarios

def handle_search_error(exception: Exception, query: str) -> str:
    """Handle search-related errors."""
    return ErrorHandler.handle_exception(
        exception,
        context=f"searching for '{query}'",
        fallback_message=f"Não consegui procurar por {query}. Tenta outra vez."
    )[0]


def handle_directions_error(exception: Exception, destination: str) -> str:
    """Handle directions-related errors."""
    return ErrorHandler.handle_exception(
        exception,
        context=f"getting directions to '{destination}'",
        fallback_message=f"Não consegui obter direções para {destination}. Verifica o destino e tenta outra vez."
    )[0]


def handle_navigation_error(exception: Exception) -> str:
    """Handle navigation-related errors."""
    return ErrorHandler.handle_exception(
        exception,
        context="starting navigation",
        fallback_message="Não consegui iniciar a navegação. Certifica-te que tens direções definidas."
    )[0]


def handle_map_control_error(exception: Exception, action: str) -> str:
    """Handle map control errors (zoom, pan, rotate, etc.)."""
    return ErrorHandler.handle_exception(
        exception,
        context=f"performing map action '{action}'",
        fallback_message=f"Não consegui {action} o mapa. Tenta outra vez."
    )[0]


# Example usage in intent handlers:
"""
try:
    # Perform some operation
    result = perform_search(query)
except Exception as e:
    # Get user-friendly message
    user_message = handle_search_error(e, query)

    return IntentResponse(
        success=False,
        message=user_message,
        data={"error": str(e)}
    )
"""
