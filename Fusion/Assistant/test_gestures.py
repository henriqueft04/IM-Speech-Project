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

# Available gestures for testing
AVAILABLE_GESTURES = [
    # Navigation/Swipe
    "swipe_left", "swipe_right", "swipe_up", "swipe_down",
    # Zoom
    "zoom_in", "zoom_out",
    # Filters
    "restaurants", "hotels", "gas_stations", "transports",
    # Street View
    "enter_street", "exit_street", "forward",
    # Selection
    "select", "up_option", "down_option",
    # Explore
    "camera",
    # Confirmation
    "thumbsup", "thumbsdown"
]


def test_gesture(assistant, gesture_name: str):
    """
    Test a single gesture by simulating its intent.

    Args:
        assistant: GoogleMapsAssistant instance
        gesture_name: Name of the gesture to test
    """
    # Map gesture names to intent names
    gesture_to_intent = {
        "swipe_left": "gesture_swipe_left",
        "swipe_right": "gesture_swipe_right",
        "swipe_up": "gesture_swipe_up",
        "swipe_down": "gesture_swipe_down",
        "zoom_in": "gesture_zoom_in",
        "zoom_out": "gesture_zoom_out",
        "restaurants": "gesture_restaurants",
        "hotels": "gesture_hotels",
        "gas_stations": "gesture_gas_stations",
        "transports": "gesture_transports",
        "enter_street": "gesture_enter_street",
        "exit_street": "gesture_exit_street",
        "forward": "gesture_forward",
        "select": "gesture_select",
        "up_option": "gesture_up_option",
        "down_option": "gesture_down_option",
        "camera": "gesture_camera",
        "thumbsup": "affirm",
        "thumbsdown": "deny",
    }

    intent = gesture_to_intent.get(gesture_name.lower())
    if not intent:
        logger.warning(f"Unknown gesture: {gesture_name}")
        logger.info(f"Available gestures: {', '.join(AVAILABLE_GESTURES)}")
        return

    logger.info(f"Testing gesture: {gesture_name} -> intent: {intent}")

    try:
        response = assistant.handle_intent(intent, 0.95, {})
        logger.info(f"Response: {response}")
    except Exception as e:
        logger.error(f"Error testing gesture {gesture_name}: {e}", exc_info=True)


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
        logger.info("  Navigation: swipe_left, swipe_right, swipe_up, swipe_down")
        logger.info("  Zoom: zoom_in, zoom_out")
        logger.info("  Filters: restaurants, hotels, gas_stations, transports")
        logger.info("  Street View: enter_street, exit_street, forward")
        logger.info("  Selection: select, up_option, down_option")
        logger.info("  Explore: camera")
        logger.info("  Confirmation: thumbsup, thumbsdown")
        logger.info("  - Type 'list' to see all available gestures")
        logger.info("  - Type 'quit' or 'exit' to stop")
        logger.info("="*60 + "\n")

        while True:
            try:
                gesture = input("\nEnter gesture name (or 'quit'): ").strip()

                if gesture.lower() in ['quit', 'exit', 'q']:
                    logger.info("Exiting test mode...")
                    break

                if gesture.lower() == 'list':
                    logger.info(f"Available gestures: {', '.join(AVAILABLE_GESTURES)}")
                    continue

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
    logger.info("Initializing Google Maps Assistant for automated tests...")
    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        logger.info("Running predefined gesture tests...")

        # Test sequence
        test_sequence = [
            ("zoom_in", 2),
            ("zoom_out", 2),
            ("swipe_right", 1),
            ("swipe_left", 1),
            ("enter_street", 3),  # Street View needs more time
            ("swipe_right", 1),   # Look around in Street View
            ("swipe_left", 1),
            ("forward", 1),       # Move forward in Street View
            ("exit_street", 2),   # Exit Street View
            ("restaurants", 2),
        ]

        import time
        for gesture, wait_time in test_sequence:
            logger.info(f"\n>>> Testing: {gesture}")
            test_gesture(assistant, gesture)
            time.sleep(wait_time)

        logger.info("\n" + "="*60)
        logger.info("Automated tests complete!")
        logger.info("="*60)

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error during automated tests: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_street_view():
    """
    Dedicated Street View test - tests enter, navigate, and exit.
    """
    logger.info("="*60)
    logger.info("STREET VIEW TEST")
    logger.info("="*60)
    logger.info("This test will:")
    logger.info("  1. Navigate to a location with Street View")
    logger.info("  2. Enter Street View mode")
    logger.info("  3. Look around (swipe gestures)")
    logger.info("  4. Move forward")
    logger.info("  5. Exit Street View")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        import time
        from infrastructure.page_objects import MapsHomePage

        # Wait for map to fully load
        logger.info("\nWaiting for map to load...")
        time.sleep(3)

        # Step 0: Navigate to a known location with good Street View coverage
        logger.info("\n[STEP 0] Navigating to a location with Street View coverage...")
        home_page = MapsHomePage(driver)

        # Search for a location known to have Street View (e.g., Times Square, Lisbon downtown)
        search_locations = [
            "Praça do Comércio, Lisboa",
            "Avenida da Liberdade, Lisboa",
            "Times Square, New York",
        ]

        search_success = False
        for location in search_locations:
            try:
                logger.info(f"  Trying: {location}")
                home_page.search(location)
                time.sleep(3)
                search_success = True
                break
            except Exception as e:
                logger.warning(f"  Failed to search {location}: {e}")
                continue

        if not search_success:
            logger.warning("Could not navigate to a specific location, will try Street View at current position")

        # Zoom in a bit to make Street View more likely to work
        logger.info("\n[STEP 0.5] Zooming in for better Street View coverage...")
        for _ in range(3):
            home_page.zoom_in()
            time.sleep(0.5)
        time.sleep(2)

        # Step 1: Enter Street View
        logger.info("\n[STEP 1] Attempting to enter Street View...")
        logger.info("  (This may take a few seconds as we try different methods)")

        success = home_page.enter_street_view()

        if success:
            logger.info("  ✓ Successfully entered Street View!")
            time.sleep(2)

            # Step 2: Look around
            logger.info("\n[STEP 2] Looking around in Street View...")

            movements = [
                ("swipe_right", "Looking right..."),
                ("swipe_right", "Looking right again..."),
                ("swipe_left", "Looking left..."),
                ("swipe_up", "Looking up..."),
                ("swipe_down", "Looking down..."),
            ]

            for gesture, description in movements:
                logger.info(f"  - {description}")
                test_gesture(assistant, gesture)
                time.sleep(1)

            # Step 3: Move forward
            logger.info("\n[STEP 3] Moving forward in Street View...")
            for i in range(2):
                logger.info(f"  - Moving forward ({i+1}/2)...")
                test_gesture(assistant, "forward")
                time.sleep(1.5)

            # Step 4: Exit Street View
            logger.info("\n[STEP 4] Exiting Street View...")
            test_gesture(assistant, "exit_street")
            time.sleep(2)

            # Verify exit
            if not home_page._is_in_street_view():
                logger.info("  ✓ Successfully exited Street View!")
            else:
                logger.warning("  ⚠ May still be in Street View")

            logger.info("\n" + "="*60)
            logger.info("STREET VIEW TEST COMPLETE!")
            logger.info("="*60)
        else:
            logger.error("\n  ✗ Could not enter Street View at this location")
            logger.info("  Possible reasons:")
            logger.info("    - No Street View coverage at current map position")
            logger.info("    - Map not zoomed in enough")
            logger.info("    - Google Maps UI changed")
            logger.info("\n  Try:")
            logger.info("    1. Manually navigate to a city center")
            logger.info("    2. Zoom in on a street")
            logger.info("    3. Run the test again")

            logger.info("\n" + "="*60)
            logger.info("STREET VIEW TEST INCOMPLETE")
            logger.info("="*60)

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error during Street View test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_street_view_manual():
    """
    Manual Street View test - waits for user to position map before testing.
    """
    logger.info("="*60)
    logger.info("MANUAL STREET VIEW TEST")
    logger.info("="*60)
    logger.info("Instructions:")
    logger.info("  1. The browser will open with Google Maps")
    logger.info("  2. Manually navigate to a street with Street View")
    logger.info("  3. Zoom in on a road")
    logger.info("  4. Press Enter in this terminal when ready")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        import time
        from infrastructure.page_objects import MapsHomePage

        # Wait for user to position map
        input("\n>>> Position the map on a street with Street View, then press Enter...")

        home_page = MapsHomePage(driver)

        logger.info("\nAttempting to enter Street View...")
        success = home_page.enter_street_view()

        if success:
            logger.info("✓ Entered Street View!")

            input("\nPress Enter to test looking around...")

            test_gesture(assistant, "swipe_right")
            time.sleep(0.5)
            test_gesture(assistant, "swipe_left")
            time.sleep(0.5)

            input("\nPress Enter to test moving forward...")

            test_gesture(assistant, "forward")
            time.sleep(1)

            input("\nPress Enter to exit Street View...")

            test_gesture(assistant, "exit_street")

            logger.info("\n✓ Test complete!")
        else:
            logger.error("✗ Could not enter Street View")
            logger.info("Try positioning the map on a main road and zooming in")

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)

    finally:
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_restaurant_to_street_view():
    """
    Complete flow test: Search restaurant -> Select first -> Zoom in -> Enter Street View
    """
    logger.info("="*60)
    logger.info("RESTAURANT TO STREET VIEW FLOW TEST")
    logger.info("="*60)
    logger.info("This test will:")
    logger.info("  1. Search for restaurants")
    logger.info("  2. Select the first restaurant from results")
    logger.info("  3. Zoom in on the restaurant location")
    logger.info("  4. Enter Street View")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        import time
        from infrastructure.page_objects import MapsHomePage, MapsSearchResultsPage, MapsPlacePage

        # Wait for map to fully load
        logger.info("\nWaiting for map to load...")
        time.sleep(3)

        home_page = MapsHomePage(driver)
        results_page = MapsSearchResultsPage(driver)
        place_page = MapsPlacePage(driver)

        # ============================================
        # STEP 1: Search for restaurants
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 1] Searching for restaurants...")
        logger.info("-"*50)

        search_queries = [
            "restaurantes em Lisboa",
            "restaurantes perto de mim",
            "restaurants nearby",
        ]

        search_success = False
        for query in search_queries:
            try:
                logger.info(f"  Searching: {query}")
                home_page.search(query)
                time.sleep(3)

                # Check if we got results
                if results_page.wait_for_results(timeout=5):
                    search_success = True
                    logger.info(f"  ✓ Found restaurant results for: {query}")
                    break
                else:
                    logger.warning(f"  No results for: {query}")
            except Exception as e:
                logger.warning(f"  Search failed for {query}: {e}")
                continue

        if not search_success:
            logger.error("  ✗ Could not find any restaurant results")
            logger.info("  Make sure you have internet connection and Google Maps is accessible")
            input("\nPress Enter to close...")
            return

        time.sleep(2)

        # ============================================
        # STEP 2: Select the first restaurant
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 2] Selecting the first restaurant...")
        logger.info("-"*50)

        # Get list of results for logging
        try:
            results = results_page.get_search_results(max_results=3)
            if results:
                logger.info(f"  Found {len(results)} results:")
                for i, result in enumerate(results[:3]):
                    logger.info(f"    {i+1}. {result.name}")
        except Exception as e:
            logger.warning(f"  Could not list results: {e}")

        # Select the first result
        select_success = results_page.select_result_by_index(0)

        if select_success:
            logger.info("  ✓ Clicked on first restaurant")
            time.sleep(3)

            # Try to get the place name
            try:
                if place_page.wait_for_place_details(timeout=5):
                    place_name = place_page.get_place_name()
                    if place_name:
                        logger.info(f"  ✓ Selected: {place_name}")
                    else:
                        logger.info("  ✓ Place selected (name not available)")
                else:
                    logger.info("  ✓ Place selected (details not loaded)")
            except Exception as e:
                logger.warning(f"  Could not get place details: {e}")
        else:
            logger.error("  ✗ Could not select the first restaurant")
            logger.info("  Will continue with current map position...")

        time.sleep(2)

        # ============================================
        # STEP 3: Zoom in on the restaurant
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 3] Zooming in on the restaurant location...")
        logger.info("-"*50)

        zoom_clicks = 5
        logger.info(f"  Zooming in {zoom_clicks} times...")

        for i in range(zoom_clicks):
            try:
                home_page.zoom_in()
                logger.info(f"    Zoom {i+1}/{zoom_clicks}")
                time.sleep(0.5)
            except Exception as e:
                logger.warning(f"    Zoom failed at step {i+1}: {e}")
                break

        logger.info("  ✓ Zoom complete")
        time.sleep(2)

        # ============================================
        # STEP 4: Enter Street View
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 4] Entering Street View...")
        logger.info("-"*50)
        logger.info("  (This may take a few seconds as we try different methods)")

        street_view_success = home_page.enter_street_view()

        if street_view_success:
            logger.info("  ✓ Successfully entered Street View!")
            time.sleep(2)

            # Bonus: Look around in Street View
            logger.info("\n  [BONUS] Looking around in Street View...")

            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains

            actions = ActionChains(driver)

            # Look right
            logger.info("    - Looking right...")
            actions.send_keys(Keys.ARROW_RIGHT).perform()
            time.sleep(0.8)
            actions.send_keys(Keys.ARROW_RIGHT).perform()
            time.sleep(0.8)

            # Look left
            logger.info("    - Looking left...")
            actions.send_keys(Keys.ARROW_LEFT).perform()
            time.sleep(0.8)

            # Look up
            logger.info("    - Looking up...")
            actions.send_keys(Keys.ARROW_UP).perform()
            time.sleep(0.8)

            # Look down
            logger.info("    - Looking down...")
            actions.send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(0.8)

            logger.info("  ✓ Street View navigation complete!")

        else:
            logger.error("  ✗ Could not enter Street View at this location")
            logger.info("  Possible reasons:")
            logger.info("    - No Street View coverage at this restaurant")
            logger.info("    - Restaurant is inside a building/mall")
            logger.info("    - Need to zoom in more")

        # ============================================
        # TEST COMPLETE
        # ============================================
        logger.info("\n" + "="*60)
        if street_view_success:
            logger.info("✓ RESTAURANT TO STREET VIEW FLOW TEST COMPLETE!")
        else:
            logger.info("⚠ TEST COMPLETED WITH ISSUES (Street View not available)")
        logger.info("="*60)

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_restaurant_flow_with_gestures():
    """
    Same flow but using gesture handlers (simulating actual gesture inputs).
    """
    logger.info("="*60)
    logger.info("RESTAURANT FLOW TEST (Using Gesture Handlers)")
    logger.info("="*60)
    logger.info("This test simulates the actual gesture flow:")
    logger.info("  1. 'restaurants' gesture -> Show restaurants filter")
    logger.info("  2. 'select' gesture -> Select first result")
    logger.info("  3. 'zoom_in' gesture -> Zoom in (multiple times)")
    logger.info("  4. 'enter_street' gesture -> Enter Street View")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        import time

        # Wait for map to fully load
        logger.info("\nWaiting for map to load...")
        time.sleep(3)

        # ============================================
        # STEP 1: Restaurants gesture
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 1] Simulating 'restaurants' gesture...")
        logger.info("-"*50)

        response = assistant.handle_intent("gesture_restaurants", 0.95, {})
        logger.info(f"  Response: {response}")
        time.sleep(3)

        # ============================================
        # STEP 2: Select gesture (first result)
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 2] Simulating 'select' gesture...")
        logger.info("-"*50)

        response = assistant.handle_intent("gesture_select", 0.95, {})
        logger.info(f"  Response: {response}")
        time.sleep(3)

        # ============================================
        # STEP 3: Zoom in gestures
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 3] Simulating 'zoom_in' gestures (5x)...")
        logger.info("-"*50)

        for i in range(5):
            response = assistant.handle_intent("gesture_zoom_in", 0.95, {})
            logger.info(f"  Zoom {i+1}/5: {response.get('message', 'OK')}")
            time.sleep(0.8)

        time.sleep(2)

        # ============================================
        # STEP 4: Enter Street View gesture
        # ============================================
        logger.info("\n" + "-"*50)
        logger.info("[STEP 4] Simulating 'enter_street' gesture...")
        logger.info("-"*50)

        response = assistant.handle_intent("gesture_enter_street", 0.95, {})
        logger.info(f"  Response: {response}")

        if response.get('success', False):
            logger.info("  ✓ Successfully entered Street View!")
            time.sleep(2)

            # Bonus: Look around using gestures
            logger.info("\n  [BONUS] Simulating look around gestures...")

            gestures = [
                ("gesture_swipe_right", "Looking right"),
                ("gesture_swipe_right", "Looking right again"),
                ("gesture_swipe_left", "Looking left"),
                ("gesture_swipe_up", "Looking up"),
                ("gesture_swipe_down", "Looking down"),
            ]

            for gesture_intent, description in gestures:
                logger.info(f"    - {description}...")
                assistant.handle_intent(gesture_intent, 0.95, {})
                time.sleep(0.8)

            logger.info("  ✓ Street View navigation complete!")
        else:
            logger.error("  ✗ Could not enter Street View")

        # ============================================
        # TEST COMPLETE
        # ============================================
        logger.info("\n" + "="*60)
        logger.info("GESTURE FLOW TEST COMPLETE!")
        logger.info("="*60)

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_map_panning():
    """
    Test map panning in all directions.
    """
    logger.info("="*60)
    logger.info("MAP PANNING TEST")
    logger.info("="*60)
    logger.info("This test will pan the map in all directions")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        import time

        # Wait for map to fully load
        logger.info("\nWaiting for map to load...")
        time.sleep(3)

        # Test panning in all directions
        directions = [
            ("swipe_right", "Panning RIGHT..."),
            ("swipe_right", "Panning RIGHT again..."),
            ("swipe_left", "Panning LEFT..."),
            ("swipe_left", "Panning LEFT again..."),
            ("swipe_up", "Panning UP..."),
            ("swipe_up", "Panning UP again..."),
            ("swipe_down", "Panning DOWN..."),
            ("swipe_down", "Panning DOWN again..."),
        ]

        for gesture, description in directions:
            logger.info(f"\n[TEST] {description}")
            test_gesture(assistant, gesture)
            time.sleep(1.5)

        logger.info("\n" + "="*60)
        logger.info("MAP PANNING TEST COMPLETE!")
        logger.info("="*60)

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_pan_debug():
    """
    Debug test for map panning - tests each method individually.
    """
    logger.info("="*60)
    logger.info("PAN DEBUG TEST")
    logger.info("="*60)
    logger.info("Testing each panning method individually")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        import time
        from infrastructure.page_objects import MapsHomePage

        # Wait for map to load
        logger.info("\nWaiting for map to load...")
        time.sleep(4)

        home_page = MapsHomePage(driver)

        # Test 1: JavaScript method
        logger.info("\n" + "-"*50)
        logger.info("[TEST 1] Testing JavaScript pan method...")
        logger.info("-"*50)
        input("Press Enter to test JS pan RIGHT...")
        result = home_page._pan_map_js("right", 3)
        logger.info(f"  JS pan right result: {result}")

        input("Press Enter to test JS pan LEFT...")
        result = home_page._pan_map_js("left", 3)
        logger.info(f"  JS pan left result: {result}")

        # Test 2: Drag method
        logger.info("\n" + "-"*50)
        logger.info("[TEST 2] Testing Drag pan method...")
        logger.info("-"*50)
        input("Press Enter to test Drag pan RIGHT...")
        result = home_page._pan_map_drag("right", 3)
        logger.info(f"  Drag pan right result: {result}")

        input("Press Enter to test Drag pan LEFT...")
        result = home_page._pan_map_drag("left", 3)
        logger.info(f"  Drag pan left result: {result}")

        # Test 3: Keyboard method
        logger.info("\n" + "-"*50)
        logger.info("[TEST 3] Testing Keyboard pan method...")
        logger.info("-"*50)
        input("Press Enter to test Keyboard pan RIGHT...")
        result = home_page._pan_map_keyboard_focused("right", 5)
        logger.info(f"  Keyboard pan right result: {result}")

        input("Press Enter to test Keyboard pan LEFT...")
        result = home_page._pan_map_keyboard_focused("left", 5)
        logger.info(f"  Keyboard pan left result: {result}")

        # Test 4: Combined method (what gesture handler uses)
        logger.info("\n" + "-"*50)
        logger.info("[TEST 4] Testing Combined pan_map method...")
        logger.info("-"*50)
        input("Press Enter to test combined pan RIGHT...")
        result = home_page.pan_map("right", 3)
        logger.info(f"  Combined pan right result: {result}")

        input("Press Enter to test combined pan UP...")
        result = home_page.pan_map("up", 3)
        logger.info(f"  Combined pan up result: {result}")

        logger.info("\n" + "="*60)
        logger.info("PAN DEBUG TEST COMPLETE!")
        logger.info("="*60)

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_street_view_navigation():
    """
    Test Street View navigation - forward, rotate left/right/up/down.
    Requires manually entering Street View first.
    """
    logger.info("="*60)
    logger.info("STREET VIEW NAVIGATION TEST")
    logger.info("="*60)
    logger.info("Instructions:")
    logger.info("  1. Browser will open with Google Maps")
    logger.info("  2. MANUALLY enter Street View (double-click on a road)")
    logger.info("  3. Press Enter in terminal when in Street View")
    logger.info("  4. Test will navigate: forward, look around")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        import time
        from infrastructure.page_objects import MapsHomePage

        # Wait for map to load
        logger.info("\nWaiting for map to load...")
        time.sleep(3)

        # Search for a location with Street View
        home_page = MapsHomePage(driver)
        logger.info("Searching for a location with Street View...")
        home_page.search("Avenida da Liberdade, Lisboa")
        time.sleep(3)

        # Zoom in
        logger.info("Zooming in...")
        for _ in range(4):
            home_page.zoom_in()
            time.sleep(0.3)
        time.sleep(2)

        input("\n>>> MANUALLY double-click on a road to enter Street View, then press Enter...")

        # Verify we're in Street View
        if not home_page._is_in_street_view():
            logger.warning("Not detected as being in Street View, but continuing test anyway...")
        else:
            logger.info("✓ In Street View mode")

        time.sleep(1)

        # Test forward movement
        logger.info("\n" + "-"*50)
        logger.info("[TEST] Moving FORWARD...")
        logger.info("-"*50)

        for i in range(3):
            logger.info(f"  Forward {i+1}/3...")
            test_gesture(assistant, "forward")
            time.sleep(1)

        input("\nPress Enter to test ROTATION...")

        # Test rotation
        logger.info("\n" + "-"*50)
        logger.info("[TEST] Rotating camera...")
        logger.info("-"*50)

        rotations = [
            ("swipe_right", "Looking RIGHT"),
            ("swipe_right", "Looking RIGHT again"),
            ("swipe_left", "Looking LEFT"),
            ("swipe_left", "Looking LEFT again"),
            ("swipe_up", "Looking UP"),
            ("swipe_down", "Looking DOWN"),
        ]

        for gesture, description in rotations:
            logger.info(f"  {description}...")
            test_gesture(assistant, gesture)
            time.sleep(0.8)

        input("\nPress Enter to test MORE FORWARD movement...")

        # More forward
        logger.info("\n" + "-"*50)
        logger.info("[TEST] More forward movement...")
        logger.info("-"*50)

        for i in range(3):
            logger.info(f"  Forward {i+1}/3...")
            test_gesture(assistant, "forward")
            time.sleep(1)

        logger.info("\n" + "="*60)
        logger.info("STREET VIEW NAVIGATION TEST COMPLETE!")
        logger.info("="*60)

        input("\nPress Enter to close...")

    except Exception as e:
        logger.error(f"Error during test: {e}", exc_info=True)

    finally:
        logger.info("Cleaning up...")
        if 'assistant' in locals():
            assistant.shutdown()
        if 'driver_manager' in locals():
            driver_manager.stop()


def test_zoom():
    """
    Test zoom in and zoom out functionality.
    """
    logger.info("="*60)
    logger.info("ZOOM TEST")
    logger.info("="*60)

    driver_manager = DriverManager()

    try:
        driver = driver_manager.start(
            headless=False,
            user_data_dir=CHROME_PROFILE_PATH
        )

        tts_service = TTSService()
        assistant = GoogleMapsAssistant(driver, tts_service)

        import time

        # Wait for map to load
        logger.info("\nWaiting for map to load...")
        time.sleep(4)

        # Test zoom in
        logger.info("\n" + "-"*50)
        logger.info("[TEST] Zooming IN (3 times)...")
        logger.info("-"*50)

        for i in range(3):
            logger.info(f"  Zoom in {i+1}/3...")
            test_gesture(assistant, "zoom_in")
            time.sleep(1)

        input("\nPress Enter to test ZOOM OUT...")

        # Test zoom out
        logger.info("\n" + "-"*50)
        logger.info("[TEST] Zooming OUT (5 times)...")
        logger.info("-"*50)

        for i in range(5):
            logger.info(f"  Zoom out {i+1}/5...")
            test_gesture(assistant, "zoom_out")
            time.sleep(1)

        logger.info("\n" + "="*60)
        logger.info("ZOOM TEST COMPLETE!")
        logger.info("="*60)

        input("\nPress Enter to close...")

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
    parser.add_argument("--auto", action="store_true", help="Run automated test sequence")
    parser.add_argument("--gesture", type=str, help="Test a specific gesture")
    parser.add_argument("--street-view", action="store_true", help="Run dedicated Street View test")
    parser.add_argument("--street-view-manual", action="store_true", help="Run manual Street View test")
    parser.add_argument("--street-view-nav", action="store_true", help="Test Street View navigation (forward, rotate)")
    parser.add_argument("--restaurant-flow", action="store_true", help="Run restaurant to Street View flow test")
    parser.add_argument("--restaurant-gestures", action="store_true", help="Run restaurant flow using gesture handlers")
    parser.add_argument("--pan-test", action="store_true", help="Run map panning test")
    parser.add_argument("--pan-debug", action="store_true", help="Debug map panning methods individually")
    parser.add_argument("--zoom-test", action="store_true", help="Test zoom in and zoom out")

    args = parser.parse_args()

    if args.zoom_test:
        test_zoom()
    elif args.street_view_nav:
        test_street_view_navigation()
    elif args.pan_debug:
        test_pan_debug()
    elif args.pan_test:
        test_map_panning()
    elif args.restaurant_flow:
        test_restaurant_to_street_view()
    elif args.restaurant_gestures:
        test_restaurant_flow_with_gestures()
    elif args.street_view:
        test_street_view()
    elif args.street_view_manual:
        test_street_view_manual()
    elif args.auto:
        run_predefined_tests()
    elif args.gesture:
        logger.info(f"Testing single gesture: {args.gesture}")
        driver_manager = DriverManager()
        try:
            driver = driver_manager.start(headless=False, user_data_dir=CHROME_PROFILE_PATH)
            tts_service = TTSService()
            assistant = GoogleMapsAssistant(driver, tts_service)
            import time
            time.sleep(2)
            test_gesture(assistant, args.gesture)
            input("\nPress Enter to close...")
        finally:
            if 'assistant' in locals():
                assistant.shutdown()
            driver_manager.stop()
    else:
        interactive_test()
