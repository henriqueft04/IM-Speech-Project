"""
Quick verification script to check gesture mappings.
Run this to verify all gestures from Gestures.xml are properly mapped.
"""

import sys
from pathlib import Path

# Add parent directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from application.services.intent_router import IntentRouter

# Gesture semantic codes from Gestures.xml
GESTURES_FROM_XML = {
    "CAMERA": "gesture_camera",
    "DOWNOL": "gesture_down_option",
    "ENTERS": "gesture_enter_street",
    "EXITS": "gesture_exit_street",
    "HOTELS": "gesture_hotels",
    "RESTAURANTS": "gesture_restaurants",
    "SELECT": "gesture_select",
    "SWIPED": "gesture_swipe_down",
    "SWIPELL": "gesture_swipe_left",
    "SWIPERR": "gesture_swipe_right",
    "SWIPEU": "gesture_swipe_up",
    "TRANSPORTS": "gesture_transports",
    "UPOR": "gesture_up_option",
    "ZOOMI": "gesture_zoom_in",
    "ZOOMO": "gesture_zoom_out",
}

def test_gesture_mapping():
    """Test that the gesture mapping in main.py correctly maps all gestures."""

    print("=" * 70)
    print("GESTURE MAPPING VERIFICATION")
    print("=" * 70)
    print()

    # Import the mapping from main.py by simulating what nlu_extractor does
    from main import nlu_extractor
    import xml.etree.ElementTree as ET
    import json

    all_ok = True
    missing_handlers = []

    for gesture_semantic, expected_intent in GESTURES_FROM_XML.items():
        # Simulate MMI message
        mmi_message = f'''<mmi:mmi xmlns:mmi="http://www.w3.org/2008/04/mmi-arch" mmi:Version="1.0">
            <mmi:ExtensionNotification mmi:context="gestures-ctx-1" mmi:requestId="gestures-id-1" mmi:source="GESTURES" mmi:target="FUSION">
                <mmi:data>
                    <emma:emma xmlns:emma="http://www.w3.org/2003/04/emma" emma:Version="1.0">
                        <emma:interpretation emma:confidence="1" emma:id="gestures-1" emma:medium="gestures" emma:mode="command">
                            <command>{{"recognized": ["GESTURES", "{gesture_semantic}"], "confidence": "0.95"}}</command>
                        </emma:interpretation>
                    </emma:emma>
                </mmi:data>
            </mmi:ExtensionNotification>
        </mmi:mmi>'''

        # Extract intent using nlu_extractor
        intent, confidence, entities, text = nlu_extractor(mmi_message)

        # Check if handler exists
        handler = IntentRouter.get_handler(intent) if intent else None

        # Verify mapping
        status = "✓" if intent == expected_intent else "✗"
        handler_status = "✓" if handler else "✗"

        if intent != expected_intent or not handler:
            all_ok = False
            if not handler:
                missing_handlers.append(intent)

        print(f"{status} {gesture_semantic:12} -> {intent:30} Handler: {handler_status}")

        if intent != expected_intent:
            print(f"  ⚠️  Expected: {expected_intent}")

    print()
    print("=" * 70)

    if all_ok:
        print("✅ ALL GESTURES MAPPED CORRECTLY!")
        print("   All 15 gestures from Gestures.xml have handlers ready.")
    else:
        print("⚠️  ISSUES FOUND:")
        if missing_handlers:
            print(f"   Missing handlers for: {', '.join(set(missing_handlers))}")
        print()
        print("   Check main.py gesture_to_intent mapping (around line 89)")

    print("=" * 70)
    print()

    return all_ok


def list_all_handlers():
    """List all registered intent handlers."""
    print("=" * 70)
    print("REGISTERED INTENT HANDLERS")
    print("=" * 70)
    print()

    handlers = IntentRouter.list_handlers()

    gesture_handlers = [h for h in handlers if h.startswith("gesture_")]
    other_handlers = [h for h in handlers if not h.startswith("gesture_")]

    print(f"Gesture Handlers ({len(gesture_handlers)}):")
    for handler in sorted(gesture_handlers):
        print(f"  • {handler}")

    print()
    print(f"Other Handlers ({len(other_handlers)}):")
    for handler in sorted(other_handlers):
        print(f"  • {handler}")

    print()
    print(f"Total: {len(handlers)} handlers registered")
    print("=" * 70)
    print()


if __name__ == "__main__":
    # Test gesture mapping
    mapping_ok = test_gesture_mapping()

    # List all handlers
    list_all_handlers()

    # Exit with error code if mapping is not OK
    sys.exit(0 if mapping_ok else 1)
