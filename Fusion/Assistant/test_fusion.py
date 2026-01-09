"""
Test script for fusion features.
Simulates fusion intents to test the complementary fusion handlers.
"""

import asyncio
import json
import xml.etree.ElementTree as ET


def create_fusion_message(fusion_intent: str) -> str:
    """
    Create a simulated MMI fusion message.

    Args:
        fusion_intent: The fusion intent name (e.g., "ZOOM_IN_UP")

    Returns:
        XML message string
    """
    command_data = {
        "recognized": ["FUSION", fusion_intent]
    }

    message = f"""<?xml version="1.0" encoding="UTF-8"?>
<mmi:mmi xmlns:mmi="http://www.w3.org/2008/04/mmi-arch" mmi:source="FUSION" mmi:target="IM">
    <mmi:extensionNotification>
        <command>{json.dumps(command_data)}</command>
    </mmi:extensionNotification>
</mmi:mmi>"""

    return message


def test_nlu_extractor():
    """Test the NLU extractor with fusion messages."""
    from main import nlu_extractor

    print("=" * 70)
    print("TESTING NLU EXTRACTOR WITH FUSION MESSAGES")
    print("=" * 70)
    print()

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

    for fusion_intent in fusion_intents:
        message = create_fusion_message(fusion_intent)
        intent, confidence, entities, text = nlu_extractor(message)

        status = "✓" if intent == fusion_intent else "✗"
        print(f"{status} {fusion_intent:20s} -> Intent: {intent}, Confidence: {confidence}")

    print()


def test_handler_registration():
    """Test that all fusion handlers are registered."""
    from application.services.intent_router import IntentRouter

    print("=" * 70)
    print("TESTING HANDLER REGISTRATION")
    print("=" * 70)
    print()

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

    for intent in fusion_intents:
        handler = IntentRouter._handlers.get(intent)
        status = "✓" if handler else "✗"
        handler_name = handler.__class__.__name__ if handler else "NOT REGISTERED"
        print(f"{status} {intent:20s} -> {handler_name}")

    print()


def print_test_instructions():
    """Print manual testing instructions."""
    print("=" * 70)
    print("MANUAL TESTING INSTRUCTIONS")
    print("=" * 70)
    print()
    print("To test fusion features manually with the full system:")
    print()
    print("1. Start the MMI server and FusionEngine")
    print("2. Make sure the updated fusion.scxml is deployed")
    print("3. Run: python main.py")
    print("4. Open Google Maps in the browser")
    print()
    print("Test each fusion combination:")
    print()

    tests = [
        ("ZOOM_IN_UP", "Say 'zoom in' while doing swipe up gesture", "Should zoom in and pan up"),
        ("ZOOM_IN_DOWN", "Say 'zoom in' while doing swipe down gesture", "Should zoom in and pan down"),
        ("ZOOM_IN_LEFT", "Say 'zoom in' while doing swipe left gesture", "Should zoom in and pan left"),
        ("ZOOM_IN_RIGHT", "Say 'zoom in' while doing swipe right gesture", "Should zoom in and pan right"),
        ("ZOOM_OUT_UP", "Say 'zoom out' while doing swipe up gesture", "Should zoom out and pan up"),
        ("ZOOM_OUT_DOWN", "Say 'zoom out' while doing swipe down gesture", "Should zoom out and pan down"),
        ("ZOOM_OUT_LEFT", "Say 'zoom out' while doing swipe left gesture", "Should zoom out and pan left"),
        ("ZOOM_OUT_RIGHT", "Say 'zoom out' while doing swipe right gesture", "Should zoom out and pan right"),
    ]

    for i, (intent, action, expected) in enumerate(tests, 1):
        print(f"{i}. {intent}")
        print(f"   Action: {action}")
        print(f"   Expected: {expected}")
        print()

    print("=" * 70)
    print()


def print_expected_log_output():
    """Print expected log output examples."""
    print("=" * 70)
    print("EXPECTED LOG OUTPUT")
    print("=" * 70)
    print()
    print("When fusion intent is triggered, you should see:")
    print()
    print("INFO - Received message from MMI")
    print("INFO - Received - Intent: ZOOM_IN_UP, Confidence: 1.00, Entities: {}, Text: ''")
    print("INFO - Zoomed in 2 level(s) via keyboard (+)")
    print("INFO - Panned map up (3 times)")
    print("INFO - Response: A aproximar e mover para cima")
    print()
    print("If handler is not registered, you'll see:")
    print("ERROR - No handler registered for intent: ZOOM_IN_UP")
    print()
    print("=" * 70)
    print()


def check_modality_files():
    """Check if the modality enum files have the required constants."""
    print("=" * 70)
    print("CHECKING MODALITY FILES")
    print("=" * 70)
    print()

    # Check Speech enum
    try:
        from scxmlgen.Modalities import Speech
        speech_attrs = [attr for attr in dir(Speech) if not attr.startswith('_')]

        required_speech = ["ZOOM_IN", "ZOOM_OUT"]
        print("Speech modality:")
        for attr in required_speech:
            status = "✓" if hasattr(Speech, attr) else "✗"
            print(f"  {status} Speech.{attr}")
    except Exception as e:
        print(f"  ✗ Error importing Speech: {e}")

    print()

    # Check Gesture enum
    try:
        from scxmlgen.Modalities import Gesture
        gesture_attrs = [attr for attr in dir(Gesture) if not attr.startswith('_')]

        required_gestures = ["SWIPE_UP", "SWIPE_DOWN", "SWIPE_LEFT", "SWIPE_RIGHT"]
        print("Gesture modality:")
        for attr in required_gestures:
            status = "✓" if hasattr(Gesture, attr) else "✗"
            print(f"  {status} Gesture.{attr}")
    except Exception as e:
        print(f"  ✗ Error importing Gesture: {e}")

    print()

    # Check Output enum
    try:
        from scxmlgen.Modalities import Output
        output_attrs = [attr for attr in dir(Output) if not attr.startswith('_')]

        required_outputs = [
            "ZOOM_IN_UP", "ZOOM_IN_DOWN", "ZOOM_IN_LEFT", "ZOOM_IN_RIGHT",
            "ZOOM_OUT_UP", "ZOOM_OUT_DOWN", "ZOOM_OUT_LEFT", "ZOOM_OUT_RIGHT"
        ]
        print("Output modality:")
        for attr in required_outputs:
            status = "✓" if hasattr(Output, attr) else "✗"
            print(f"  {status} Output.{attr}")
            if not hasattr(Output, attr):
                print(f"       You need to add this to the Output enum!")
    except Exception as e:
        print(f"  ✗ Error importing Output: {e}")

    print()
    print("=" * 70)
    print()


def main():
    """Run all tests."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "FUSION FEATURE TEST SUITE" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Test 1: Check modality files
    check_modality_files()

    # Test 2: NLU Extractor
    try:
        test_nlu_extractor()
    except Exception as e:
        print(f"✗ NLU Extractor test failed: {e}")
        print()

    # Test 3: Handler Registration
    try:
        test_handler_registration()
    except Exception as e:
        print(f"✗ Handler Registration test failed: {e}")
        print()

    # Test 4: Expected log output
    print_expected_log_output()

    # Test 5: Manual testing instructions
    print_test_instructions()

    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 25 + "TEST COMPLETE" + " " * 30 + "║")
    print("╚" + "═" * 68 + "╝")
    print()


if __name__ == "__main__":
    main()
