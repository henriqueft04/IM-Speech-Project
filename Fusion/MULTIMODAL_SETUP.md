# Multimodal Fusion System - Complete Setup Guide

This guide explains how to run the complete multimodal Google Maps assistant that combines **voice commands** and **gesture inputs** through fusion.

---

## System Architecture

```
┌──────────────┐         ┌─────────────┐
│   Kinect     │         │ Microphone  │
│  (Gestures)  │         │  (Speech)   │
└──────┬───────┘         └──────┬──────┘
       │                        │
       │ [GESTURES][...]        │ Speech Audio
       │                        │
       ▼                        ▼
┌────────────────┐       ┌─────────────┐
│  Gesture App   │       │    ASR      │
│ GenericGestures│       │  (External) │
│  Modality.exe  │       │             │
└──────┬─────────┘       └──────┬──────┘
       │                        │
       │ MMI WebSocket          │ [SPEECH][...]
       │                        │
       └────────┬───────────────┘
                │
         ┌──────▼───────┐
         │  MMI Server  │
         │  (Port 8000  │
         │   Port 8005) │
         └──────┬───────┘
                │
      ┌─────────┴──────────┐
      │                    │
 ┌────▼──────┐      ┌──────▼───────┐
 │   RASA    │      │   Fusion     │
 │    NLU    │      │   Engine     │
 │(Port 5005)│      │   (SCXML)    │
 └────┬──────┘      └──────┬───────┘
      │                    │
      │ NLU Results        │ [FUSION][...]
      └─────────┬──────────┘
                │
         ┌──────▼───────┐
         │   Fusion     │
         │  Assistant   │
         │  (Python)    │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │  WebDriver   │
         │ Google Maps  │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │  TTS System  │
         │ (WebSocket   │
         │  Port 8083)  │
         └──────────────┘
```

---

## Components Running

When you run `start.bat`, the following 5 components are launched:

### 1. **FUSION** - FusionEngine (Port 8001)
- SCXML-based state machine
- Routes gesture and voice events
- Combines modalities into fusion events
- **File**: `FusionEngine/FusionEngine.jar`

### 2. **CLIENT** - MMI Framework (Port 8000/8005)
- HTTP server on port 8000
- WebSocket server on port 8005
- Message broker for all modalities
- **File**: `IM/mmiframeworkV2.jar`

### 3. **RASA** - NLU Service (Port 5005)
- Natural Language Understanding
- Processes voice commands in Portuguese
- Extracts intents and entities
- **Command**: `python -m rasa run --enable-api`

### 4. **WEBAPP** - Web Interface (Port 8082/8083)
- HTTPS server on port 8082
- TTS WebSocket server on port 8083
- Provides browser interface
- **File**: `WebAppAssistantV2/server.py`

### 5. **SERVER** - Python Assistant
- Main orchestration logic
- Handles multimodal commands
- Controls Google Maps via Selenium
- Sends TTS feedback
- **File**: `Assistant/main.py`

---

## Quick Start

### Option 1: Automatic Start (Recommended)

Simply run:
```batch
start.bat
```

This will:
1. Launch all 5 components in separate windows
2. Automatically open the web interface in your browser
3. Initialize Google Maps in Chrome

### Option 2: Manual Start

If you need to start components individually:

```batch
# 1. Start FusionEngine
cd FusionEngine
start.bat

# 2. Start MMI Server
cd IM
start.bat

# 3. Start RASA
python\python.exe -m rasa run --enable-api -m rasaDemo\models\ --cors "*"

# 4. Start WebApp
cd WebAppAssistantV2
venv\Scripts\activate
python server.py

# 5. Start Assistant
cd Assistant
venv\Scripts\activate
python main.py

# 6. Open browser
openpage.bat
```

---

## Adding Gesture Input

To enable gesture recognition, you also need to run:

### 6. **GESTURES** - Kinect Application

```batch
cd GenericGesturesModality-2023
GenericGesturesModality.exe
```

**Requirements:**
- Kinect v2 sensor connected
- Kinect Runtime installed
- Visual Gesture Builder runtime installed

**Supported Gestures** (15 total):
- **Zoom**: ZoomIn, ZoomOut
- **Navigation**: SwipeUp, SwipeDown, SwipeLeft, SwipeRight
- **Filters**: Restaurants, Hotels, Transports, Camera
- **Selection**: Select, UpOption, DownOption
- **Street View**: EnterStreet, ExitStreet

---

## Multimodal Interaction Examples

### Voice Only
```
User says: "procurar restaurantes em Aveiro"
→ [SPEECH][SEARCH_LOCATION]
→ [FUSION][SEARCH_LOCATION]
→ Assistant searches for restaurants in Aveiro
→ TTS: "Encontrei 30 restaurantes em Aveiro"
```

### Gesture Only
```
User gestures: Restaurants filter
→ [GESTURES][RESTAURANTS]
→ [FUSION][GESTURE_RESTAURANTS]
→ Assistant clicks restaurants filter
→ TTS: "A mostrar restaurantes na área"
```

### Combined Usage (Sequential)
```
1. User says: "procurar hotéis em Lisboa"
   → Search for hotels in Lisbon
   → TTS: "Encontrei 50 hotéis em Lisboa"

2. User gestures: ZoomIn
   → Zoom into map
   → TTS: "Aproximado"

3. User says: "selecionar o primeiro"
   → Select first result
   → TTS: "Selecionado: Hotel XYZ"

4. User gestures: Select
   → Open details
   → TTS: "A mostrar detalhes"
```

---

## Supported Voice Commands

### Search & Navigation
- "procurar [location]" - Search for location
- "encontrar [place]" - Find place
- "direções para [destination]" - Get directions
- "como chego a [place]" - How to get to place
- "iniciar navegação" - Start navigation
- "parar navegação" - Stop navigation

### Map Controls
- "aproximar" / "mais perto" - Zoom in
- "afastar" / "mais longe" - Zoom out
- "vista de satélite" - Satellite view
- "mostrar trânsito" - Show traffic
- "recentrar" - Recenter map

### Location Information
- "mostrar detalhes" - Show place details
- "mostrar avaliações" - Show reviews
- "mostrar fotos" - Show photos
- "horário de abertura" - Opening hours

### Selection
- "selecionar o primeiro" - Select first result
- "opção [número]" - Select option by number

---

## Supported Gestures

### Map Navigation
- **SwipeUp**: Pan up / Move forward in street view
- **SwipeDown**: Pan down / Move backward in street view
- **SwipeLeft**: Pan left / Rotate left in street view
- **SwipeRight**: Pan right / Rotate right in street view

### Zoom
- **ZoomIn**: Zoom in on map
- **ZoomOut**: Zoom out on map

### Filters
- **Restaurants**: Show restaurants
- **Hotels**: Show hotels
- **Transports**: Show public transport
- **Camera**: Open "Things to do" / Activities

### Selection & Navigation
- **Select**: Select first result or current item
- **UpOption**: Navigate up in lists
- **DownOption**: Navigate down in lists

### Street View
- **EnterStreet**: Enter Street View mode
- **ExitStreet**: Exit Street View mode

---

## Checking System Status

### Verify All Components Are Running

Look for these windows:

1. **FUSION** window:
   ```
   SCXML Fusion Engine
   Listening to https://0.0.0.0:8001
   ```

2. **CLIENT** window:
   ```
   Listening to https://0.0.0.0:8000
   Started listener bound to [0.0.0.0:8000]
   ```

3. **RASA** window:
   ```
   Rasa server is up and running
   ```

4. **WEBAPP** window:
   ```
   Servidor HTTPS na porta 8082...
   TTS WebSocket server running on ws://127.0.0.1:8083
   ```

5. **SERVER** window:
   ```
   INFO - Connected to MMI server
   INFO - TTS: Boas! Eu sou a Assistente de Google Maps. Como te posso ajudar?
   ```

### Browser Console (F12)

You should see:
```
TTS WebSocket connected to ws://127.0.0.1:8083
```

And you should **HEAR** the welcome message in Portuguese!

---

## Troubleshooting

### No TTS Audio?
- ✅ Check browser console shows "TTS WebSocket connected"
- ✅ Verify WEBAPP window shows "TTS WebSocket client connected"
- ✅ Unmute browser audio
- ✅ Ensure you're using Chrome or Edge (Web Speech API required)

### Voice Commands Not Working?
- ✅ Check RASA window shows "Rasa server is up and running"
- ✅ Verify RASA is listening on port 5005
- ✅ Check browser console for RASA connection errors
- ✅ Test RASA directly: `curl http://localhost:5005/model/parse -d '{"text":"procurar restaurantes"}'`

### Gestures Not Working?
- ✅ Verify Kinect is connected and powered
- ✅ Check GenericGesturesModality.exe is running
- ✅ Confirm gesture is being recognized (green checkmark in app)
- ✅ Check CLIENT window for incoming gesture messages
- ✅ Verify FusionEngine is routing gesture events

### Google Maps Not Responding?
- ✅ Ensure Chrome window opened by Selenium
- ✅ Check SERVER window for errors
- ✅ Verify Google Maps loaded fully
- ✅ Check for Selenium WebDriver errors

### Port Already in Use?
If you get "port already in use" errors:
```batch
# Find process using port
netstat -ano | findstr :8000
netstat -ano | findstr :8005
netstat -ano | findstr :5005
netstat -ano | findstr :8082

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

## File Structure

```
Fusion/
├── start.bat                          # Main launch script
├── openpage.bat                       # Opens web interface
├── MULTIMODAL_SETUP.md               # This file
│
├── FusionEngine/                      # Multimodal fusion logic
│   ├── FusionEngine.jar
│   ├── fusion.scxml                   # Fusion state machine
│   └── start.bat
│
├── IM/                                # MMI message broker
│   ├── mmiframeworkV2.jar
│   ├── keys/keystore2.jks            # SSL certificates
│   └── start.bat
│
├── rasaDemo/                          # NLU service
│   ├── domain.yml                     # Intents and entities
│   ├── models/                        # Trained RASA models
│   └── config.yml
│
├── WebAppAssistantV2/                 # Web interface + TTS
│   ├── server.py                      # HTTPS + WebSocket server
│   ├── index.htm / appGui.htm         # Browser interface
│   ├── cert.pem, key.pem              # SSL certificates
│   └── venv/                          # Python environment
│
├── Assistant/                         # Main application logic
│   ├── main.py                        # Entry point
│   ├── config/
│   │   └── settings.py                # Configuration
│   ├── application/
│   │   ├── assistant.py               # Core orchestration
│   │   ├── intent_handlers/           # Intent implementations
│   │   │   ├── search_handler.py
│   │   │   ├── navigation_handler.py
│   │   │   ├── gesture_handler.py     # Gesture-specific handlers
│   │   │   └── ...
│   │   └── services/
│   │       ├── tts_service.py         # Text-to-speech
│   │       └── ...
│   └── venv/                          # Python environment
│
└── GenericGesturesModality-2023/      # Kinect gesture recognition
    ├── GenericGesturesModality.exe
    ├── Gestures.xml                   # Gesture definitions
    └── Gestures.gbd                   # Gesture database

```

---

## Next Steps

### Current Capabilities
- ✅ Voice commands (30+ intents)
- ✅ Gesture recognition (15 gestures)
- ✅ Multimodal routing via FusionEngine
- ✅ TTS feedback in Portuguese
- ✅ Google Maps control via Selenium

### Future Enhancements
To implement true multimodal integration (not just routing):

1. **Temporal Fusion**: Buffer inputs from multiple modalities within time window
2. **Semantic Integration**: Combine partial inputs (e.g., "zoom here" + point gesture)
3. **Disambiguation**: Resolve conflicts between modalities
4. **Context Management**: Track gaze, attention, and interaction history
5. **Gesture+Speech Fusion**: Support complementary inputs like:
   - "Go here" + point gesture
   - "Zoom" + hand gesture indicating amount
   - "Compare these two" + select two places

---

## Technical Details

### Message Flow Example

**Voice Command: "procurar restaurantes"**

1. User speaks → ASR system
2. ASR → MMI Server: `[SPEECH]["procurar restaurantes"]`
3. MMI → RASA: `POST /model/parse {"text": "procurar restaurantes"}`
4. RASA → MMI: `{"intent": {"name": "search_location"}, "entities": [{"entity": "location", "value": "restaurantes"}]}`
5. MMI → FusionEngine: `[SPEECH][SEARCH_LOCATION]`
6. FusionEngine → Assistant: `[FUSION][SEARCH_LOCATION]`
7. Assistant → Selenium: Search "restaurantes" on Google Maps
8. Assistant → TTS: "Encontrei X restaurantes"
9. TTS → Browser: JSON message via WebSocket
10. Browser: Speaks via Web Speech API

**Gesture: Restaurants Filter**

1. User gestures → Kinect
2. Kinect → GenericGesturesModality.exe
3. App → MMI Server: `[GESTURES][RESTAURANTS]`
4. MMI → FusionEngine: `[GESTURES][RESTAURANTS]`
5. FusionEngine → Assistant: `[FUSION][GESTURE_RESTAURANTS]`
6. Assistant → Selenium: Click restaurants filter button
7. Assistant → TTS: "A mostrar restaurantes"
8. TTS → Browser: JSON message
9. Browser: Speaks

---

## Support & Documentation

- **Intent Handlers**: See `Assistant/application/intent_handlers/`
- **RASA Training Data**: See `rasaDemo/data/nlu.yml`
- **Gesture Definitions**: See `GenericGesturesModality-2023/Gestures.xml`
- **Fusion Logic**: See `FusionEngine/fusion.scxml`

---

Last Updated: 2026-01-07
