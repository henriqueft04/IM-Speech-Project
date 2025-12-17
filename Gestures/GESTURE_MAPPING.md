# Gesture Mapping Reference

This document maps the Kinect gestures to their corresponding actions on Google Maps.

## Gesture Configuration

When training gestures in GenericGesturesModality, use these EXACT names (case-sensitive):

| Gesture Name | Event Sent | Action on Google Maps |
|--------------|------------|----------------------|
| **Restaurants** | `[GESTURES][RESTAURANTS]` | Click "Restaurantes" filter button |
| **Hotels** | `[GESTURES][HOTELS]` | Click "Hotéis" filter button |
| **Transports** | `[GESTURES][TRANSPORTS]` | Click "Transportes públicos" filter button |
| **Camera** | `[GESTURES][CAMERA]` | Open **"Coisas a fazer"** (Explore/Activities) menu |
| **EnterStreet** | `[GESTURES][ENTERSTREET]` | Enter Street View mode |
| **ExitStreet** | `[GESTURES][EXITSTREET]` | Exit Street View mode (press Escape) |
| **Forward** | `[GESTURES][FORWARD]` | Move forward in Street View |
| **SwipeRight** | `[GESTURES][SWIPERIGHT]` | **Rotate camera right** in Street View (Arrow Right) |
| **SwipeLeft** | `[GESTURES][SWIPELEFT]` | **Rotate camera left** in Street View (Arrow Left) |
| **SwipeUp** | `[GESTURES][SWIPEUP]` | **Rotate camera up** in Street View (Arrow Up) |
| **SwipeDown** | `[GESTURES][SWIPEDOWN]` | **Rotate camera down** in Street View (Arrow Down) |
| **Select** | `[GESTURES][SELECT]` | Select first search result |
| **UpOption** | `[GESTURES][UPOPTION]` | Navigate up in search results (Arrow Up) |
| **DownOption** | `[GESTURES][DOWNOPTION]` | Navigate down in search results (Arrow Down) |

## Event Flow

```
Kinect Gesture Recognition (GenericGesturesModality.exe)
    ↓
    Sends: [GESTURES][RESTAURANTS]
    ↓
FusionEngine (fusion.scxml)
    ↓
    Processes gesture and forwards to IM
    ↓
IM/MMI Framework
    ↓
    Routes to Python Assistant
    ↓
Assistant (gesture_handler.py)
    ↓
    Executes corresponding handler
    ↓
Google Maps (via Selenium WebDriver)
    ↓
    Performs action (click button, pan, zoom, etc.)
```

## Files Modified

1. **Gestures/FusionEngine/fusion.scxml**
   - Added transitions for all 15 gestures in the `<state id="main">` section
   - Added state definitions for each gesture at the end of the file

2. **Gestures/Assistant/application/intent_handlers/gesture_handler.py**
   - Added handler classes for all new gestures:
     - `TransportsFilterHandler`
     - `DragUpHandler`
     - `CameraHandler`
     - `EnterStreetHandler`
     - `ExitStreetHandler`
     - `ForwardHandler`
     - `SelectHandler`
     - `UpOptionHandler`
     - `DownOptionHandler`

## Running the System

1. Start all components using `Gestures\start.bat`:
   - FusionEngine
   - IM (MMI Framework)
   - Assistant (Python backend)

2. Manually run `GenericGesturesModality.exe`

3. Train your gestures with the exact names listed above

4. Perform gestures and watch them control Google Maps!

## Troubleshooting

- **Gesture not recognized**: Check GenericGesturesModality console for recognition confidence
- **FUSION skips gesture**: Verify gesture name matches exactly (case matters!)
- **No action on Maps**: Check Assistant console for errors
- **Handler not found**: Ensure gesture name in Gestures.xml matches the event name

## Notes

- Case matters! Use exact capitalization: `Restaurants`, not `restaurants`
- The Kinect app will send `[GESTURES][RESTAURANTS]`, which becomes `GESTURE_RESTAURANTS` in the intent router
- All handlers are registered automatically via the `@IntentRouter.register()` decorator
