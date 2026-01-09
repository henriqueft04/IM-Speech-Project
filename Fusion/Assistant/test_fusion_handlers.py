"""
Test script for fusion handlers - Direct handler testing without Kinect.
This script allows you to test fusion functionality by directly invoking handlers.
"""

import sys
from pathlib import Path

# Add the Assistant directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import DriverManager
from config.settings import CHROME_PROFILE_PATH
from application.intent_handlers.base_handler import IntentContext
from application.services.intent_router import IntentRouter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_menu():
    """Display the test menu."""
    print("\n" + "=" * 70)
    print("FUSION HANDLER TEST MENU")
    print("=" * 70)
    print("\nZoom In + Swipe Combinations:")
    print("  1. ZOOM_IN_UP      - Zoom in and pan up")
    print("  2. ZOOM_IN_DOWN    - Zoom in and pan down")
    print("  3. ZOOM_IN_LEFT    - Zoom in and pan left")
    print("  4. ZOOM_IN_RIGHT   - Zoom in and pan right")
    print("\nZoom Out + Swipe Combinations:")
    print("  5. ZOOM_OUT_UP     - Zoom out and pan up")
    print("  6. ZOOM_OUT_DOWN   - Zoom out and pan down")
    print("  7. ZOOM_OUT_LEFT   - Zoom out and pan left")
    print("  8. ZOOM_OUT_RIGHT  - Zoom out and pan right")
    print("\nOther Options:")
    print("  9. Test all handlers sequentially")
    print("  0. Exit")
    print("=" * 70)


def test_fusion_intent(driver, intent_name: str):
    """
    Test a specific fusion intent by invoking its handler directly.

    Args:
        driver: WebDriver instance
        intent_name: Name of the fusion intent to test
    """
    print(f"\n{'=' * 70}")
    print(f"Testing: {intent_name}")
    print(f"{'=' * 70}")

    try:
        # Create intent context
        context = IntentContext(
            intent=intent_name,
            confidence=1.0,
            entities={},
            driver=driver,
            metadata={}
        )

        # Route the intent to the handler
        response = IntentRouter.handle_intent(context)

        # Display results
        if response.success:
            print(f"✓ SUCCESS: {response.message}")
        else:
            print(f"✗ FAILED: {response.message}")

        if response.data:
            print(f"  Data: {response.data}")

    except Exception as e:
        print(f"✗ ERROR: {e}")
        logger.error(f"Error testing {intent_name}", exc_info=True)

    print(f"{'=' * 70}\n")


def test_all_handlers(driver):
    """Test all fusion handlers sequentially."""
    fusion_intents = [
        "ZOOM_IN_UP",
        "ZOOM_IN_DOWN",
        "ZOOM_IN_LEFT",
        "ZOOM_IN_RIGHT",
        "ZOOM_OUT_UP",
        "ZOOM_OUT_DOWN",
        "ZOOM_OUT_LEFT",
        "ZOOM_OUT_RIGHT"
    ]

    print(f"\n{'=' * 70}")
    print("TESTING ALL FUSION HANDLERS")
    print(f"{'=' * 70}\n")

    import time
    for intent in fusion_intents:
        test_fusion_intent(driver, intent)
        time.sleep(1)  # Small delay between tests

    print(f"\n{'=' * 70}")
    print("ALL TESTS COMPLETED")
    print(f"{'=' * 70}\n")


def verify_handlers_registered():
    """Verify all fusion handlers are registered."""
    print(f"\n{'=' * 70}")
    print("VERIFYING HANDLER REGISTRATION")
    print(f"{'=' * 70}\n")

    fusion_intents = [
        "ZOOM_IN_UP",
        "ZOOM_IN_DOWN",
        "ZOOM_IN_LEFT",
        "ZOOM_IN_RIGHT",
        "ZOOM_OUT_UP",
        "ZOOM_OUT_DOWN",
        "ZOOM_OUT_LEFT",
        "ZOOM_OUT_RIGHT"
    ]

    all_registered = True
    for intent in fusion_intents:
        handler = IntentRouter._handlers.get(intent)
        if handler:
            print(f"✓ {intent:20s} -> {handler.__class__.__name__}")
        else:
            print(f"✗ {intent:20s} -> NOT REGISTERED")
            all_registered = False

    print(f"\n{'=' * 70}\n")

    if not all_registered:
        print("⚠ WARNING: Not all handlers are registered!")
        print("Make sure fusion_handler.py is imported in __init__.py\n")
        return False

    return True


def main():
    """Main test function."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "FUSION HANDLER DIRECT TEST TOOL" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝\n")

    # Verify handlers are registered
    if not verify_handlers_registered():
        print("Please fix handler registration before testing.")
        return

    # Initialize WebDriver
    print("Initializing Chrome WebDriver...")
    driver_manager = DriverManager()

    try:
        # Start driver
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        # Navigate to Google Maps
        print("Opening Google Maps...")
        driver.get("https://www.google.com/maps")

        input("\nPress ENTER when Google Maps is loaded and ready...")

        # Menu mapping
        intent_map = {
            "1": "ZOOM_IN_UP",
            "2": "ZOOM_IN_DOWN",
            "3": "ZOOM_IN_LEFT",
            "4": "ZOOM_IN_RIGHT",
            "5": "ZOOM_OUT_UP",
            "6": "ZOOM_OUT_DOWN",
            "7": "ZOOM_OUT_LEFT",
            "8": "ZOOM_OUT_RIGHT",
            "9": "ALL"
        }

        # Main test loop
        while True:
            print_menu()
            choice = input("\nEnter your choice (0-9): ").strip()

            if choice == "0":
                print("\nExiting test tool. Goodbye!")
                break

            elif choice == "9":
                test_all_handlers(driver)

            elif choice in intent_map:
                intent_name = intent_map[choice]
                test_fusion_intent(driver, intent_name)

            else:
                print("\n✗ Invalid choice. Please enter a number between 0-9.")

            if choice != "0" and choice != "9":
                input("\nPress ENTER to continue...")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n✗ Fatal error: {e}")

    finally:
        # Clean up
        print("\nCleaning up...")
        if 'driver_manager' in locals():
            driver_manager.stop()
        print("Cleanup complete.")


if __name__ == "__main__":
    main()
