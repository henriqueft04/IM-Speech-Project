# Fusion Project - Setup Instructions

This guide will help you set up the Fusion multimodal assistant project on your machine.

---

## Prerequisites

### Required Software

1. **Python 3.10** (REQUIRED - not 3.11, 3.12, or 3.14)
   - Download from: https://www.python.org/downloads/release/python-31011/
   - During installation, check "Add Python to PATH"
   - Verify installation: `python --version` should show `Python 3.10.x`

2. **Java Runtime Environment (JRE)**
   - Required for FusionEngine and MMI Server
   - Download from: https://www.java.com/download/

3. **Google Chrome**
   - Required for Selenium WebDriver
   - Download from: https://www.google.com/chrome/

### Optional (for Gestures)

4. **Kinect v2 Sensor** + **Kinect Runtime**
   - Only needed if you want gesture recognition
   - Download Kinect Runtime: https://www.microsoft.com/en-us/download/details.aspx?id=44559

---

## Step 1: Clone/Download the Project

Make sure you have the complete `Fusion` folder with all subdirectories:

```
Fusion/
├── venv/                    # Virtual environment (will be created)
├── FusionEngine/           # Multimodal fusion logic
├── IM/                     # MMI message broker
├── WebAppAssistantV2/      # Web interface
├── Assistant/              # Main Python application
├── GenericGesturesModality-2023/  # Gesture recognition (optional)
├── rasaDemo/               # NLU models
├── start.bat               # Main launch script
└── requirements.txt        # Python dependencies
```

---

## Step 2: Install RASA

RASA is the Natural Language Understanding engine for voice commands.

### Option A: Using pip (Recommended)

Open Command Prompt and run:

```bash
pip install rasa
```

**This will take 5-10 minutes** - RASA is a large package with many dependencies.

### Option B: Already Installed?

Check if RASA is already installed:

```bash
python -m rasa --version
```

If you see version info (e.g., "Rasa Version: 3.6.x"), you're good to go!

---

## Step 3: Set Up Virtual Environment

Navigate to the Fusion directory and install dependencies:

```bash
cd path\to\Fusion
python -m pip install -r requirements.txt
```

**Note**: If RASA isn't installed globally, uncomment line 18 in `requirements.txt` first:

```python
# Change this:
# rasa~=3.5.0

# To this:
rasa~=3.5.0
```

---

## Step 4: Verify Setup

Check that all dependencies are installed in the venv:

```bash
venv\Scripts\activate
python -c "import selenium, websockets; print('Dependencies OK!')"
rasa --version
```

You should see:
- "Dependencies OK!"
- RASA version information

---

## Step 5: Run the System

Simply run:

```batch
start.bat
```

This will launch **5 windows**:

1. **FUSION** - Multimodal fusion engine
2. **CLIENT** - MMI message broker
3. **RASA** - Natural Language Understanding server
4. **WEBAPP** - Web interface with TTS
5. **SERVER** - Google Maps assistant

Your browser will automatically open to the web interface.

---

## Expected Output

### When Everything is Working:

**FUSION window:**
```
SCXML Fusion Engine
Listening to https://0.0.0.0:8001
```

**CLIENT window:**
```
Listening to https://0.0.0.0:8000
Started listener bound to [0.0.0.0:8000]
```

**RASA window:**
```
Rasa server is up and running
```

**WEBAPP window:**
```
Servidor HTTPS na porta 8082...
TTS WebSocket server running on ws://127.0.0.1:8083
```

**SERVER window:**
```
INFO - Connected to MMI server
INFO - TTS: Boas! Eu sou a Assistente de Google Maps. Como te posso ajudar?
```

**Browser:**
- Should automatically open to `https://<your-ip>:8082/appGui.htm`
- You'll see a security warning (self-signed certificate) - click "Advanced" → "Proceed"
- Console should show: `TTS WebSocket connected to ws://127.0.0.1:8083`
- You should **HEAR** the welcome message in Portuguese!

---

## Troubleshooting

### "python is not recognized..."
- Python 3.10 is not in your PATH
- Reinstall Python 3.10 and check "Add Python to PATH"

### "java is not recognized..."
- Java is not installed or not in PATH
- Install Java JRE and restart your terminal

### "Module not found: rasa"
- RASA not installed in venv
- Run: `venv\Scripts\activate` then `pip install rasa`

### "Port already in use"
- Another instance is running
- Close all terminal windows and try again
- Or find and kill the process:
  ```
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```

### RASA Won't Install
- Make sure you're using Python 3.10 (not 3.11, 3.12, or 3.14)
- RASA 3.x requires Python 3.10 or 3.11 specifically

### No TTS Audio
- Check browser console (F12) for errors
- Verify WEBAPP window shows "TTS WebSocket client connected"
- Make sure browser audio isn't muted
- Use Chrome or Edge (Web Speech API required)

### Gestures Not Working
- Make sure Kinect v2 is connected and powered
- Install Kinect Runtime if not already installed
- Run `GenericGesturesModality.exe` manually after starting the system

---

## Testing Voice Commands

Once everything is running, try saying (in Portuguese):

- "procurar restaurantes em Aveiro"
- "direções para Lisboa"
- "aproximar" (zoom in)
- "afastar" (zoom out)
- "mostrar trânsito"

You should see Google Maps respond and hear TTS feedback!

---

## Common Voice Commands

### Search & Navigation
- "procurar [location]" - Search for location
- "encontrar [place]" - Find place
- "direções para [destination]" - Get directions
- "iniciar navegação" - Start navigation

### Map Controls
- "aproximar" - Zoom in
- "afastar" - Zoom out
- "mostrar trânsito" - Show traffic
- "vista de satélite" - Satellite view

### Information
- "mostrar detalhes" - Show place details
- "mostrar avaliações" - Show reviews
- "horário de abertura" - Opening hours

---

## Stopping the System

To stop all components:

1. Press any key in each terminal window
2. OR close all terminal windows
3. Close the browser tab

---

## Project Structure

- **FusionEngine/** - SCXML-based multimodal fusion
- **IM/** - MMI framework (message broker)
- **rasaDemo/** - RASA NLU models for Portuguese
- **WebAppAssistantV2/** - Browser interface + TTS WebSocket server
- **Assistant/** - Main Python app (Google Maps automation)
- **GenericGesturesModality-2023/** - Kinect gesture recognition

---

## Additional Resources

- **RASA Documentation**: https://rasa.com/docs/
- **Selenium Documentation**: https://www.selenium.dev/documentation/
- **Project Documentation**: See `MULTIMODAL_SETUP.md` for detailed architecture info

---

## Need Help?

If you encounter issues not covered here:

1. Check all terminal windows for error messages
2. Verify Python version: `python --version` (must be 3.10.x)
3. Verify RASA: `rasa --version`
4. Check browser console (F12) for JavaScript errors

---

**Last Updated**: 2026-01-07
**Python Version**: 3.10 (REQUIRED)
**RASA Version**: 3.5.x - 3.6.x
