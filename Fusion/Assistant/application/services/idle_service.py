"""
Idle detection service for proactive engagement.
Tracks user activity and prompts when inactive.
"""

import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class IdleService:
    """
    Service to track user activity and provide idle prompts.

    Monitors time since last user interaction and can trigger
    proactive messages when user has been inactive.
    """

    def __init__(self, idle_threshold: int = 120):
        """
        Initialize idle service.

        Args:
            idle_threshold: Seconds of inactivity before considering user idle (default: 120s / 2 minutes)
        """
        self.idle_threshold = idle_threshold
        self.last_activity_time = time.time()
        self.idle_prompt_sent = False
        logger.info(f"IdleService initialized with threshold: {idle_threshold}s")

    def record_activity(self):
        """Record that user activity has occurred."""
        self.last_activity_time = time.time()
        self.idle_prompt_sent = False
        logger.debug("User activity recorded")

    def get_idle_duration(self) -> float:
        """
        Get how long user has been idle.

        Returns:
            Seconds since last activity
        """
        return time.time() - self.last_activity_time

    def is_idle(self) -> bool:
        """
        Check if user is currently idle.

        Returns:
            True if user has been inactive longer than threshold
        """
        return self.get_idle_duration() > self.idle_threshold

    def should_prompt(self) -> bool:
        """
        Check if we should send an idle prompt to user.

        Returns:
            True if user is idle and we haven't already prompted
        """
        if self.is_idle() and not self.idle_prompt_sent:
            self.idle_prompt_sent = True
            return True
        return False

    def get_idle_message(self) -> str:
        """
        Get an appropriate idle prompt message.

        Returns:
            Idle prompt message in Portuguese
        """
        idle_duration = self.get_idle_duration()

        if idle_duration < 180:  # Less than 3 minutes
            return "Não te vejo a usar o sistema. Precisas de ajuda?"
        elif idle_duration < 300:  # Less than 5 minutes
            return "Ainda aí? Posso ajudar com alguma coisa?"
        else:
            return "Se precisares de ajuda, é só dizer!"

    def reset(self):
        """Reset idle tracking."""
        self.last_activity_time = time.time()
        self.idle_prompt_sent = False
        logger.info("Idle service reset")
