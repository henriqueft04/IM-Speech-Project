"""
Test script to simulate gesture inputs without actual hardware.
Run this to test if the Selenium actions work correctly.
"""

import sys
from pathlib import Path

# Add the Assistant directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

import logging
from config import DriverManager
from application.assistant import GoogleMapsAssistant
from application.services import TTSService
from config.settings import CHROME_PROFILE_PATH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_gesture(assistant, gesture_name: str):
    """
    Simulate a gesture and test the handler.

    Args:
        assistant: GoogleMapsAssistant instance
        gesture_name: Name of the gesture to simulate
    """
    # Map gestures to intents (same logic as nlu_extractor)
    gesture_to_intent = {
        "thumbsup": "affirm",
        "thumbs_up": "affirm",
        "thumbsdown": "deny",
        "thumbs_down": "deny",
    }

    gesture_lower = gesture_name.lower()
    intent = gesture_to_intent.get(gesture_lower, f"gesture_{gesture_lower}")

    logger.info(f"\n{'='*50}")
    logger.info(f"Testing gesture: {gesture_name}")
    logger.info(f"Mapped to intent: {intent}")
    logger.info(f"{'='*50}")

    response = assistant.handle_intent(
        intent=intent,
        confidence=1.0,
        entities={"gesture": gesture_lower},
        metadata={"text": ""}
    )

    logger.info(f"Response: {response}")
    return response


def interactive_test():
    """
    Interactive test mode - enter gesture names to test them.
    """
    logger.info("Initializing Google Maps Assistant for testing...")
    driver_manager = DriverManager()

    try:
        # Start driver
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        # Initialize TTS service (won't actually speak without websocket)
        tts_service = TTSService()

        # Initialize assistant
        assistant = GoogleMapsAssistant(driver, tts_service)

        logger.info("Assistant initialized successfully!")
        logger.info("\n" + "="*60)
        logger.info("GESTURE TEST MODE")
        logger.info("="*60)
        logger.info("Available gestures to test:")
        logger.info("  - swipe_left, swipe_right, swipe_up, swipe_down")
        logger.info("  - zoom_in, zoom_out")
        logger.info("  - restaurants, hotels, gas_stations")
        logger.info("  - thumbsup, thumbsdown (for affirm/deny)")
        logger.info("  - Type 'quit' or 'exit' to stop")
        logger.info("="*60 + "\n")

        while True:
            try:
                gesture = input("\nEnter gesture name (or 'quit'): ").strip()

                if gesture.lower() in ['quit', 'exit', 'q']:
                    logger.info("Exiting test mode...")
                    break

                if not gesture:
                    continue

                test_gesture(assistant, gesture)

                # Small pause to see the action
                input("Press Enter to continue...")

            except KeyboardInterrupt:
                logger.info("\nTest interrupted by user")
                break

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()
        logger.info("Test complete")


def run_predefined_tests():
    """
    Run a predefined sequence of gesture tests.
    """
    logger.info("Initializing Google Maps Assistant for testing...")
    driver_manager = DriverManager()

    try:
        # Start driver
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        logger.info("Assistant initialized successfully!")

        # List of gestures to test
        gestures_to_test = [
            "swipe_right",
            "swipe_left",
            "swipe_up",
            "swipe_down",
            "zoom_in",
            "zoom_out",
            # "restaurants",  # Uncomment to test filters
            # "hotels",
        ]

        import time

        for gesture in gestures_to_test:
            test_gesture(assistant, gesture)
            time.sleep(2)  # Wait 2 seconds between tests

        logger.info("\nAll predefined tests completed!")
        input("Press Enter to close...")

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test gesture handlers")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run predefined tests automatically"
    )
    parser.add_argument(
        "--gesture",
        type=str,
        help="Test a single specific gesture"
    )

    args = parser.parse_args()

    if args.auto:
        run_predefined_tests()
    elif args.gesture:
        # Quick single gesture test
        import time
        driver_manager = DriverManager()
        try:
            driver = driver_manager.start(headless=False, user_data_dir=CHROME_PROFILE_PATH)
            tts_service = TTSService()
            assistant = GoogleMapsAssistant(driver, tts_service)

            # Wait for Google Maps to fully load
            logger.info("Waiting for Google Maps to load...")
            time.sleep(10)
            input("Press Enter when Google Maps is ready to test the gesture...")

            test_gesture(assistant, args.gesture)
            input("Press Enter to close...")
        finally:
            if 'assistant' in locals():
                assistant.shutdown()
            driver_manager.stop()
    else:
        interactive_test()
