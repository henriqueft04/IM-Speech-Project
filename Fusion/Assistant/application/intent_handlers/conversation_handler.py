"""
Intent handler for conversational intents.
Handles greet, goodbye, thanks.
"""

import logging

from application.intent_handlers.base_handler import (
    BaseIntentHandler,
    IntentContext,
    IntentResponse
)
from application.services.intent_router import IntentRouter

logger = logging.getLogger(__name__)


@IntentRouter.register("greet")
class GreetHandler(BaseIntentHandler):
    """Handler for greeting the user."""

    supported_intents = ["greet"]
    requires_confirmation = False
    confidence_threshold = 0.60

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Greet the user.

        Args:
            context: Intent context

        Returns:
            IntentResponse with greeting
        """
        return IntentResponse(
            success=True,
            message="Boas! Como é que te posso ajudar com o Google Maps?"
        )


@IntentRouter.register("goodbye")
class GoodbyeHandler(BaseIntentHandler):
    """Handler for saying goodbye."""

    supported_intents = ["goodbye"]
    requires_confirmation = False
    confidence_threshold = 0.60

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Say goodbye to the user.

        Args:
            context: Intent context

        Returns:
            IntentResponse with goodbye message
        """
        return IntentResponse(
            success=True,
            message="Adeus! Até à próxima!"
        )


@IntentRouter.register("thanks")
class ThanksHandler(BaseIntentHandler):
    """Handler for acknowledging thanks."""

    supported_intents = ["thanks"]
    requires_confirmation = False
    confidence_threshold = 0.60

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Acknowledge user thanks.

        Args:
            context: Intent context

        Returns:
            IntentResponse with acknowledgment
        """
        return IntentResponse(
            success=True,
            message="De nada! Estou aqui sempre que precisares."
        )


@IntentRouter.register("affirm")
class AffirmHandler(BaseIntentHandler):
    """Handler for affirmative responses (yes/sim)."""

    supported_intents = ["affirm"]
    requires_confirmation = False
    confidence_threshold = 0.50

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle affirmative response.

        Args:
            context: Intent context

        Returns:
            IntentResponse with acknowledgment
        """
        return IntentResponse(
            success=True,
            message="Ok, confirmado!"
        )


@IntentRouter.register("deny")
class DenyHandler(BaseIntentHandler):
    """Handler for negative responses (no/não)."""

    supported_intents = ["deny"]
    requires_confirmation = False
    confidence_threshold = 0.50

    def execute(self, context: IntentContext) -> IntentResponse:
        """
        Handle negative response.

        Args:
            context: Intent context

        Returns:
            IntentResponse with acknowledgment
        """
        return IntentResponse(
            success=True,
            message="Ok, cancelado."
        )
