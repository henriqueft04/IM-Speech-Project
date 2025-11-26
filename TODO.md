# Project TODO List

## 🟢 Medium Priority - Missing Features

### 5. Implement Traffic Control Handlers
**Files to create/modify:**
- `Voice\Assistant\application\intent_handlers\map_control_handler.py`

**Missing handlers:**
```python
@IntentRouter.register("show_traffic")
class ShowTrafficHandler(BaseIntentHandler):
    # Implementation needed
    pass

@IntentRouter.register("hide_traffic")
class HideTrafficHandler(BaseIntentHandler):
    # Implementation needed
    pass
```

### 6. Implement Pan/Move Map Handlers
**Files to create:**
- `Voice\Assistant\application\intent_handlers\map_navigation_handler.py`

**Missing handlers:**
```python
@IntentRouter.register("pan_map")
class PanMapHandler(BaseIntentHandler):
    # Handle: move_left, move_right, move_up, move_down
    # Entities: direction (north, south, east, west, left, right, up, down)
    pass
```

### 7. Implement Place Selection Handler
```python
@IntentRouter.register("select_place")
class SelectPlaceHandler(BaseIntentHandler):
    # Handle: "select first result", "choose number 2"
    # Entities: ordinal (first, second, third, 1, 2, 3)
    pass
```

### 8. Add Page Object Methods
**File:** `Voice\Assistant\infrastructure\page_objects\maps_home_page.py`

**Missing methods:**
- `toggle_traffic_layer(show: bool) -> bool`
- `pan_map(direction: Direction, distance: int = 100) -> bool`

## 🔵 Low Priority - Enhancements

### 9. Add Unit Tests
- Create `Voice\Assistant\tests\` directory
- Test intent handlers
- Test page objects
- Test intent router

### 10. Improve Error Handling
- Add retry logic for Selenium failures
- Better error messages for users
- Logging for debugging

### 11. Add More NLU Training Examples
- Improve accuracy by adding more examples to `Voice\rasaDemo\data\nlu.yml`
- Test with different phrasings

### 12. Configuration Improvements
- Add environment variables support
- Create `.env.example` file
- Better documentation for settings

## 📋 Completed

✅ Assistant dependencies installed (Selenium, websockets, etc.)
✅ Clean architecture implemented
✅ Core intent handlers working:
  - Search locations
  - Get directions
  - Start/stop navigation
  - Zoom in/out
  - Change map type
  - Show place details
  - Show reviews/photos
  - Opening hours
  - Help/Cancel handlers
✅ Page Object Model implemented
✅ Intent Router with registry pattern
✅ Confirmation service
✅ TTS service
✅ WebSocket integration

## Immediate Next Steps

1. **Get `mmiframeworkV2.jar`** - Contact professor/classmates
2. **Install RASA**: `pip install --user rasa`
3. **Fix domain.yml** - Update intents list
4. **Train model**: `rasa train nlu`
5. **Test system** - Run all 3 components and test voice commands

---

Last updated: 2025-11-25
