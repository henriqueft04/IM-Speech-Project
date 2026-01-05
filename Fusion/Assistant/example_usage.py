"""
Example usage of the Google Maps Assistant without WebSocket.
Useful for testing and development.
"""

import sys
import os
from pathlib import Path

# Add the Assistant directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

import logging
from config.selenium_config import DriverManager
from application.assistant import GoogleMapsAssistant
from application.services.tts_service import TTSService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Standalone example demonstrating the assistant's capabilities.
    """
    # Initialize driver
    logger.info("Starting Chrome...")
    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(headless=False)

        # Initialize assistant
        logger.info("Initializing assistant...")
        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        # Example commands to test (Portuguese)
        test_commands = [
            # Search - using a less famous location to trigger results page
            {
                "intent": "search_location",
                "confidence": 0.95,
                "entities": {"location": "restaurantes em Lisboa"}
            },
            # # Zoom in
            {
                "intent": "zoom_in",
                "confidence": 0.90,
                "entities": {"zoom_level": "muito"}
            },
            # # Show traffic
            {
                "intent": "change_map_type",
                "confidence": 0.92,
                "entities": {"map_type": "trânsito"}
            },
            # # Change map type
            {
                "intent": "change_map_type",
                "confidence": 0.88,
                "entities": {"map_type": "satélite"}
            },

        ]

        # Execute test commands
        for i, command in enumerate(test_commands, 1):
            logger.info(f"\n--- Test Command {i} ---")
            logger.info(f"Intent: {command['intent']}")
            logger.info(f"Entities: {command['entities']}")

            # Handle the intent
            response = assistant.handle_intent(
                intent=command["intent"],
                confidence=command["confidence"],
                entities=command["entities"]
            )

            logger.info(f"Response: {response}")

            # Wait a bit between commands
            import time
            time.sleep(3)

        # Keep browser open for manual inspection
        input("\nPress Enter to close the browser and exit...")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

    finally:
        # Cleanup
        logger.info("Shutting down...")
        if 'assistant' in locals():
            assistant.shutdown()
        driver_manager.stop()
        logger.info("Done!")


if __name__ == "__main__":
    main()
