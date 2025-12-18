# How to Start the Complete Gestures System

To run the full multimodal gesture system with TTS audio, you need to start 3 components:

## 1. Start the FusionEngine

Open a command prompt:
```bash
cd "c:\Users\henri\OneDrive - Universidade de Aveiro\Desktop\IM-Speech-Project\Gestures\FusionEngine"
start.bat
```

**Expected output:**
```
Websocket Server is running ...
Listening to https://0.0.0.0:8000
```

---

## 2. Start the WebApp (for TTS audio)

Open a **second** command prompt:
```bash
cd "c:\Users\henri\OneDrive - Universidade de Aveiro\Desktop\IM-Speech-Project\Gestures\WebAppAssistantV2"
python server.py
```

**Expected output:**
```
Servidor HTTPS na porta 8082...
TTS WebSocket server running on ws://127.0.0.1:8083
```

Then open your browser and navigate to:
```
https://127.0.0.1:8082/index.htm
```

**Accept the self-signed certificate warning** (this is normal for local development)

The browser will connect to the TTS WebSocket and you'll see:
```
TTS WebSocket connected to ws://127.0.0.1:8083
```

---

## 3. Start the Python Assistant

Open a **third** command prompt:
```bash
cd "c:\Users\henri\OneDrive - Universidade de Aveiro\Desktop\IM-Speech-Project\Gestures\Assistant"
python main.py
```

**Expected output:**
```
INFO - Assistant initialized successfully
INFO - Connected to MMI server
INFO - TTS: Boas! Eu sou a Assistente de Google Maps. Como te posso ajudar?
```

**You should now HEAR the welcome message** through your browser!

---

## 4. Start the Gesture Recognition

Open a **fourth** command prompt:
```bash
cd "c:\Users\henri\OneDrive - Universidade de Aveiro\Desktop\IM-Speech-Project\Gestures\GenericGesturesModality-2023"
# Run your gesture recognition application
```

Or double-click the gesture recognition executable.

---

## System Architecture

```
┌─────────────────────┐
│ Gesture Recognition │ (Kinect/Camera)
│  (C# Application)   │
└──────────┬──────────┘
           │ MMI Messages
           ↓
┌─────────────────────┐
│   FusionEngine      │ Port 8000 (MMI WebSocket)
│   (Java/SCXML)      │
└──────────┬──────────┘
           │ MMI Messages
           ↓
┌─────────────────────┐
│  Python Assistant   │ Receives gestures,
│     (main.py)       │ controls Google Maps
└──────────┬──────────┘
           │ TTS Messages
           ↓ (port 8083)
┌─────────────────────┐
│  WebApp + Browser   │ Port 8082 (HTTPS)
│   (server.py)       │ Port 8083 (TTS WebSocket)
│                     │ Plays audio via Web Speech API
└─────────────────────┘
```

---

## Testing the System

Once all 4 components are running:

1. **Check browser console** - should show "TTS WebSocket connected"
2. **Perform a gesture** (e.g., Hotels gesture)
3. **You should:**
   - See the gesture logged in Python Assistant
   - See Google Maps update (show hotels)
   - **HEAR** the TTS response ("A mostrar hotéis na área")

---

## Troubleshooting

### No Audio?
- ✅ Check browser console for "TTS WebSocket connected"
- ✅ Verify `server.py` shows "TTS WebSocket client connected"
- ✅ Check browser audio isn't muted
- ✅ Verify Web Speech API is available (works in Chrome/Edge)

### Gestures not working?
- ✅ Check FusionEngine logs for gesture messages
- ✅ Verify Python Assistant shows "Gesture recognized: XXX"
- ✅ See [GESTURE_STATUS.md](../GESTURE_STATUS.md) for mapping

### Google Maps not responding?
- ✅ Ensure Chrome is running (started by Python Assistant)
- ✅ Check Python logs for Selenium errors
- ✅ Verify Google Maps loaded in browser

---

## Quick Start Script

Create a `start_all.bat` file to launch everything at once:

```batch
@echo off
title Starting Gesture System
echo Starting all components...

start "FusionEngine" cmd /k "cd FusionEngine && start.bat"
timeout /t 3

start "WebApp TTS" cmd /k "cd WebAppAssistantV2 && python server.py"
timeout /t 3

start "Python Assistant" cmd /k "cd Assistant && python main.py"

echo All components started!
echo.
echo Open browser to: https://127.0.0.1:8082/index.htm
echo.
pause
```

---

Last updated: 2025-12-18
