"""
Intent router with handler registry.
Routes intents to appropriate handlers using a registry pattern.
"""

import logging
from typing import Dict, Type, Optional

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)

logger = logging.getLogger(__name__)


class IntentRouter:
    """
    Routes intents to registered handlers.

    Provides a registry pattern for intent handlers with decorator-based
    registration for clean, extensible intent handling.
    """

    # Class-level handler registry
    _handlers: Dict[str, BaseIntentHandler] = {}

    @classmethod
    def register(cls, *intents: str):
        """
        Decorator to register a handler class for specific intents.

        Usage:
            @IntentRouter.register("search_location", "find_place")
            class SearchLocationHandler(BaseIntentHandler):
                ...

        Args:
            intents: Intent names this handler should handle

        Returns:
            Decorator function
        """
        def decorator(handler_class: Type[BaseIntentHandler]):
            handler_instance = handler_class()

            # Register this handler for each intent
            for intent in intents:
                if intent in cls._handlers:
                    logger.warning(
                        f"Overwriting existing handler for intent '{intent}': "
                        f"{cls._handlers[intent]} -> {handler_instance}"
                    )
                cls._handlers[intent] = handler_instance
                logger.info(f"Registered {handler_class.__name__} for intent '{intent}'")

            return handler_class

        return decorator

    @classmethod
    def register_handler(cls, handler: BaseIntentHandler):
        """
        Manually register a handler instance.

        Args:
            handler: Handler instance to register
        """
        for intent in handler.supported_intents:
            if intent in cls._handlers:
                logger.warning(
                    f"Overwriting existing handler for intent '{intent}'"
                )
            cls._handlers[intent] = handler
            logger.info(f"Registered {handler.__class__.__name__} for intent '{intent}'")

    @classmethod
    def get_handler(cls, intent: str) -> Optional[BaseIntentHandler]:
        """
        Get the handler for a specific intent.

        Args:
            intent: Intent name

        Returns:
            Handler instance or None if not found
        """
        return cls._handlers.get(intent)

    @classmethod
    def handle_intent(cls, context: IntentContext) -> IntentResponse:
        """
        Route an intent to its handler and execute it.

        Args:
            context: Intent context with all necessary data

        Returns:
            IntentResponse from the handler

        Raises:
            ValueError: If no handler found for intent
        """
        handler = cls.get_handler(context.intent)

        if handler is None:
            error_msg = f"No handler registered for intent '{context.intent}'"
            logger.error(error_msg)
            return IntentResponse(
                success=False,
                message=f"I don't know how to handle '{context.intent}'",
                data={"error": error_msg}
            )

        # Check confidence threshold
        if context.confidence < handler.confidence_threshold:
            logger.info(
                f"Confidence {context.confidence:.2f} below threshold "
                f"{handler.confidence_threshold} for {context.intent}"
            )
            # Return response indicating confirmation needed
            return IntentResponse(
                success=False,
                message=f"Did you want to {context.intent}?",
                requires_follow_up=True,
                follow_up_data={
                    "handler": handler,
                    "context": context,
                    "reason": "low_confidence"
                }
            )

        # Execute the handler
        try:
            logger.info(
                f"Executing {handler.__class__.__name__} for intent '{context.intent}' "
                f"(confidence: {context.confidence:.2f})"
            )
            response = handler.execute(context)
            return response

        except Exception as e:
            logger.error(f"Error executing handler for '{context.intent}': {e}", exc_info=True)
            return IntentResponse(
                success=False,
                message=f"Sorry, I encountered an error while trying to {context.intent}",
                data={"error": str(e)}
            )

    @classmethod
    def list_handlers(cls) -> Dict[str, str]:
        """
        Get a dictionary of registered intents and their handlers.

        Returns:
            Dict mapping intent names to handler class names
        """
        return {
            intent: handler.__class__.__name__
            for intent, handler in cls._handlers.items()
        }

    @classmethod
    def clear_registry(cls):
        """Clear all registered handlers (useful for testing)."""
        cls._handlers.clear()
        logger.info("Handler registry cleared")
