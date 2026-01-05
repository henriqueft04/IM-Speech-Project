# Google Maps Voice Assistant

A voice-controlled Google Maps assistant built with Python, Selenium, and Rasa NLU. This project provides a clean, maintainable architecture for controlling Google Maps through voice commands.

## Features

### Search & Navigation
- Search for locations and places
- Get directions with multiple transport modes (driving, walking, transit, cycling)
- Start/stop turn-by-turn navigation

### Map Controls
- Zoom in/out with variable intensity
- Pan in any direction
- Change map type (satellite, terrain, default)
- Show/hide traffic layer
- Recenter map to current location

### Location Information
- View place details
- Read reviews
- View photos
- Check opening hours

## Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
IM-Duarte/
├── config/              # Configuration and driver setup
├── domain/              # Business entities and enums
├── application/         # Use cases and services
│   ├── intent_handlers/ # Intent-specific logic
│   └── services/        # Router, confirmation, TTS
├── infrastructure/      # External interfaces (Selenium)
│   └── page_objects/    # Page Object Model for Google Maps
├── rasa/                # Rasa NLU configuration
└── main.py              # Entry point
```

### Key Design Patterns

- **Page Object Model**: Maintainable Selenium interactions
- **Handler Registry**: Extensible intent routing
- **Dependency Injection**: Testable components
- **Strategy Pattern**: Flexible action handling
- **Confirmation Middleware**: Action-specific confirmations

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install ChromeDriver

The Selenium WebDriver requires ChromeDriver to control Chrome:

**Option A: Automatic (recommended)**
```bash
pip install webdriver-manager
```

**Option B: Manual**
- Download from: https://chromedriver.chromium.org/
- Add to PATH or specify path in config

### 3. Configure Settings

Edit `config/settings.py` to customize:

```python
# Chrome profile for persistent login (optional)
CHROME_PROFILE_PATH = "~/.config/google-chrome/Default"

# WebSocket URL for your MMI server
MMI_URL = "wss://127.0.0.1:8005/IM/USER1/APP"

# NLU confidence thresholds
HIGH_CONFIDENCE_THRESHOLD = 0.80
MEDIUM_CONFIDENCE_THRESHOLD = 0.60
```

### 4. Set up Rasa (If not already configured)

The `rasa/nlu.yml` file contains all intent definitions. To train your Rasa model:

```bash
# In your Rasa project directory
rasa train nlu
```

Copy the trained model to your Rasa server.

## Usage

### Running the Assistant

```bash
python main.py
```

This will:
1. Start a Chrome browser with Google Maps
2. Connect to the MMI WebSocket server
3. Listen for voice commands
4. Execute actions and provide TTS feedback

### Voice Command Examples

**Search & Navigation:**
- "Search for Eiffel Tower"
- "Find coffee shops near me"
- "Get directions to the airport"
- "Navigate to home by walking"
- "Start navigation"

**Map Controls:**
- "Zoom in"
- "Zoom out a lot"
- "Move left"
- "Pan north"
- "Switch to satellite view"
- "Show traffic"
- "Recenter map"

**Location Info:**
- "Show place details"
- "What are the reviews?"
- "Show photos"
- "Is it open now?"

**General:**
- "Help" - List available commands
- "Cancel" - Cancel current operation

## Adding New Intents

The architecture makes it easy to add new features:

### 1. Define Intent in Rasa NLU

Edit `rasa/nlu.yml`:

```yaml
- intent: close_place
  examples: |
    - close this place
    - dismiss
    - go back
```

### 2. Create Handler

Create `application/intent_handlers/my_handler.py`:

```python
from application.services.intent_router import IntentRouter
from application.intent_handlers.base_handler import BaseIntentHandler, IntentContext, IntentResponse

@IntentRouter.register("close_place")
class ClosePlaceHandler(BaseIntentHandler):
    supported_intents = ["close_place"]
    requires_confirmation = False
    confidence_threshold = 0.70

    def execute(self, context: IntentContext) -> IntentResponse:
        # Your implementation here
        context.driver.back()

        return IntentResponse(
            success=True,
            message="Went back"
        )
```

### 3. Import Handler

Add to `application/intent_handlers/__init__.py`:

```python
from . import my_handler
```

That's it! The handler is automatically registered and ready to use.

## Configuration Options

### Confidence Thresholds

In `config/settings.py`:

```python
HIGH_CONFIDENCE_THRESHOLD = 0.80  # Execute directly
MEDIUM_CONFIDENCE_THRESHOLD = 0.60  # Ask for confirmation
LOW_CONFIDENCE_THRESHOLD = 0.45  # Minimum to process
```

### Action-Specific Confirmation

Control which intents require confirmation:

```python
REQUIRES_CONFIRMATION = {
    "start_navigation": True,  # Always confirm
    "search_location": False,  # Never confirm (unless low confidence)
    # ... more intents
}
```

### Browser Settings

```python
# Run headless (no visible browser)
driver = driver_manager.start(headless=True)

# Use specific Chrome profile
driver = driver_manager.start(user_data_dir="~/.config/google-chrome/Profile 1")
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_intent_router.py

# Run with coverage
pytest --cov=application --cov=infrastructure
```

## Troubleshooting

### Chrome doesn't start
- Ensure ChromeDriver is installed and in PATH
- Check Chrome version matches ChromeDriver version
- Try running without headless mode to see errors

### Elements not found
- Google Maps UI changes frequently
- Check `infrastructure/page_objects/` for locators
- Use browser dev tools to inspect elements
- Update XPath/CSS selectors as needed

### WebSocket connection fails
- Verify MMI server is running
- Check SSL certificate settings
- Ensure firewall allows connections

### Low NLU confidence
- Add more training examples in `rasa/nlu.yml`
- Retrain Rasa model
- Adjust confidence thresholds in settings

## Best Practices

### Selenium
- ✅ Use explicit waits (WebDriverWait)
- ✅ Implement retry logic for transient failures
- ✅ Use Page Object Model for maintainability
- ❌ Avoid `time.sleep()` (use `WebDriverWait` instead)
- ❌ Don't use absolute XPath (fragile)

### Intent Handlers
- Keep handlers focused on single responsibility
- Validate required entities before execution
- Return meaningful feedback messages
- Handle errors gracefully

### Code Organization
- Put business logic in handlers, not page objects
- Use domain entities for data modeling
- Keep configuration separate from code
- Write tests for critical paths

## Project Structure Details

### `config/`
- `selenium_config.py`: WebDriver setup and management
- `settings.py`: Application configuration constants

### `domain/`
- `entities.py`: Data models (Location, Route, PlaceDetails, MapState)
- `enums.py`: Enumerations (TransportMode, MapType, Direction, ZoomLevel)

### `application/`
- `assistant.py`: Main orchestrator
- `intent_handlers/`: Intent-specific business logic
- `services/`: Cross-cutting services (routing, confirmation, TTS)

### `infrastructure/`
- `page_objects/`: Selenium page objects for Google Maps
- `selenium_helpers.py`: Utility functions and decorators

### `rasa/`
- `nlu.yml`: Intent and entity definitions with training examples

## Contributing

When adding features:
1. Follow existing code patterns
2. Add type hints
3. Write docstrings
4. Create tests
5. Update this README

## License

[Your License Here]

## Acknowledgments

- Inspired by the MDJD Projects YouTube assistant
- Built with modern Python best practices
- Designed for educational purposes in multimodal interaction
