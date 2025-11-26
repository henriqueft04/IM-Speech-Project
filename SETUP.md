# IM-Speech-Project Setup Guide

This guide will help you set up and run the Google Maps Voice Assistant project.

## Prerequisites

✅ **Already Installed:**
- Python 3.12 (confirmed at `C:\Python312\python.exe`)
- Java 23 (confirmed, system-wide)
- Git

## Project Structure

```
IM-Speech-Project/
├── Voice/
│   ├── Assistant/          # Main Google Maps assistant code
│   ├── rasaDemo/           # RASA NLU configuration
│   ├── mmiframeworkV2/     # MMI Framework (multimodal interaction)
│   └── WebAppAssistantV2/  # Web interface for voice input
└── readme.txt
```

## Setup Steps

### 1. Install Python Dependencies for Assistant

```powershell
cd Voice\Assistant
pip install --user -r requirements.txt
```

**Status:** ✅ Completed

### 2. Install RASA (NLU Engine)

```powershell
pip install --user rasa
```

This will take some time (5-10 minutes) as RASA has many dependencies.

### 4. Train RASA Model (After installing RASA)

```powershell
cd Voice\rasaDemo
rasa train nlu
```

This will create a trained model in `Voice\rasaDemo\models\` directory.

### 5. Update RASA Domain Configuration

The current `domain.yml` is outdated. You need to update it to match the intents in `data\nlu.yml`.

**Current issues:**
- `domain.yml` has old intents (`light_switch`, `change_color`)
- Should have Google Maps intents (`search_location`, `get_directions`, etc.)

**Fix:** Update [Voice\rasaDemo\domain.yml](Voice/rasaDemo/domain.yml) with proper intents.

## Running the System

The system consists of 3 components that need to run simultaneously:

### Component 1: MMI Framework Server

```powershell
cd Voice\mmiframeworkV2
java -jar mmiframeworkV2.jar
```

**Status:** ⚠️ Blocked - need `mmiframeworkV2.jar` file

**Alternative:** A batch file was created at `Voice\mmiframeworkV2\start_mmi.bat`

### Component 2: RASA NLU Server

```powershell
cd Voice\rasaDemo
rasa run --enable-api --cors "*" --port 5005
```

This starts the RASA NLU server on port 5005.

### Component 3: Google Maps Assistant

```powershell
cd Voice\Assistant
python main.py
```

This will:
1. Open Chrome browser with Google Maps
2. Connect to MMI server (wss://127.0.0.1:8005/IM/USER1/APP)
3. Listen for voice commands
4. Execute actions on Google Maps

### Component 4 (Optional): Web Interface

```powershell
cd Voice\WebAppAssistantV2\kws__
python server.py
```

Then open `http://localhost:8000` in your browser for the voice input interface.

## Configuration

### Chrome Profile (Optional)

To persist Google Maps login:

Edit [Voice\Assistant\config\settings.py](Voice/Assistant/config/settings.py):

```python
# Change from:
CHROME_PROFILE_PATH = None

# To your Chrome profile:
CHROME_PROFILE_PATH = "C:\\Users\\henri\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
```

### Confidence Thresholds

Adjust in [Voice\Assistant\config\settings.py](Voice/Assistant/config/settings.py):

```python
HIGH_CONFIDENCE_THRESHOLD = 0.80  # Execute directly
MEDIUM_CONFIDENCE_THRESHOLD = 0.60  # Ask for confirmation
LOW_CONFIDENCE_THRESHOLD = 0.45  # Minimum to process
```

## Troubleshooting

### Python/Java in Voice/ directories

**Issue:** The `Voice\python\` and `Voice\Java\` directories are incomplete and missing executables.

**Solution:** Use system Python and Java instead (both are properly installed).

### MMI Framework JAR Missing

**Issue:** `mmiframeworkV2.jar` file is missing.

**Solution:**
1. Check with your course materials
2. Ask your professor or classmates
3. Check university Moodle/course website

### RASA Not Found

**Issue:** `rasa: command not found`

**Solution:**
```powershell
pip install --user rasa
# Then add to PATH: C:\Users\henri\AppData\Roaming\Python\Python312\Scripts
```

### WebSocket Connection Failed

**Issue:** Assistant can't connect to MMI server.

**Solution:**
1. Ensure MMI Framework is running first
2. Check firewall settings
3. Verify SSL certificates

## Testing Voice Commands

Once all components are running, try these commands (in Portuguese):

### Search
- "Procurar Lisboa"
- "Encontrar café perto de mim"

### Directions
- "Direções para casa"
- "Como chego ao aeroporto"

### Map Controls
- "Aproximar"
- "Afastar muito"
- "Vista de satélite"

### Place Information
- "Mostrar avaliações"
- "Mostrar fotos"
- "Está aberto agora?"

## Project Status

### ✅ Implemented Features
- Search locations
- Get directions (multiple transport modes)
- Start/stop navigation
- Zoom in/out
- Change map type
- Show place details, reviews, photos
- Opening hours

### ⚠️ Missing Implementations
- Show/hide traffic layer
- Pan map (move left/right/up/down)
- Select place from search results
- Show alternative routes

### 🔧 Configuration Issues
- RASA domain.yml needs updating
- Missing MMI Framework JAR file

## Next Steps

1. **Get mmiframeworkV2.jar** from course materials
2. **Install RASA:** `pip install --user rasa`
3. **Update domain.yml** to match NLU intents
4. **Train RASA model:** `rasa train nlu`
5. **Test the system** with all 3 components running

## Additional Resources

- [Project README](Voice/Assistant/README.md) - Detailed architecture documentation
- RASA Documentation: https://rasa.com/docs/
- Selenium Documentation: https://selenium-python.readthedocs.io/

## Contact

For issues specific to this project setup, contact your professor or check course materials.
