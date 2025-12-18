# Troubleshooting Guide

Common issues and solutions for the Gesture Recognition System.

---

## ❌ Error: "The remote computer refused the network connection"

### Problem
```
ConnectionRefusedError: [WinError 1225] The remote computer refused the network connection
```

### Cause
The Python Assistant is trying to connect to the FusionEngine, but the FusionEngine isn't running yet.

### Solution
**Start components in the correct order:**

1. **First:** Start FusionEngine
   ```bash
   cd FusionEngine
   start.bat
   ```
   Wait for: `Websocket Server is running ... Listening to https://0.0.0.0:8000`

2. **Second:** Start WebApp TTS Server
   ```bash
   cd WebAppAssistantV2
   python server.py
   ```
   Wait for: `TTS WebSocket server running on ws://127.0.0.1:8083`

3. **Third:** Start Python Assistant
   ```bash
   cd Assistant
   python main.py
   ```
   Wait for: `Connected to MMI server`

**Or use:** `start_all.bat` which prompts you to wait for each component.

---

## ❌ Error: "No such file or directory" (cert.pem)

### Problem
```
FileNotFoundError: [Errno 2] No such file or directory
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
```

### Cause
The WebApp TTS Server needs SSL certificates but they're missing.

### Solution
✅ **Already fixed!** The SSL certificates have been copied from the Voice project.

If you still see this error, manually copy them:
```bash
copy ..\Voice\WebAppAssistantV2\cert.pem WebAppAssistantV2\
copy ..\Voice\WebAppAssistantV2\key.pem WebAppAssistantV2\
```

---

## 🔇 No Audio / Can't Hear TTS

### Problem
Google Maps responds to gestures but no audio is heard.

### Possible Causes & Solutions

#### 1. WebApp Server Not Running
**Check:** Is `python server.py` running?

**Solution:** Start the WebApp server:
```bash
cd WebAppAssistantV2
python server.py
```

#### 2. Browser Not Connected
**Check:** Is the browser open to `https://127.0.0.1:8082/index.htm`?

**Solution:**
1. Open browser to `https://127.0.0.1:8082/index.htm`
2. Accept SSL certificate warning (click "Advanced" → "Proceed")
3. Open browser console (F12)
4. Look for: `TTS WebSocket connected to ws://127.0.0.1:8083`

#### 3. Browser Audio Muted
**Check:** Is the browser tab muted?

**Solution:** Unmute the tab (check speaker icon on browser tab)

#### 4. Web Speech API Not Available
**Check:** Are you using Chrome or Edge?

**Solution:** Use Chrome or Microsoft Edge (Firefox has limited Web Speech API support)

#### 5. Server Not Sending to Browser
**Check:** Python logs show `DEBUG - Sent TTS directly to browser`?

**Solution:** The TTS service should log when sending. If missing, check `tts_service.py` is using direct mode (not MMI mode).

---

## 🚫 Gestures Being SKIPPED

### Problem
Logs show:
```
SKIPED: [GESTURES][DOWNOL] / null
```

### Cause
Gesture semantic code doesn't map to a Python handler.

### Solution
✅ **Already fixed!** All 15 gestures are now mapped in `main.py`.

If you add new gestures, update the mapping in [`main.py`](Assistant/main.py) (around line 89):
```python
gesture_to_intent = {
    "newgesture": "gesture_new_gesture",
    # ... add your mapping here
}
```

---

## 🗺️ Google Maps Not Responding

### Problem
Gestures are recognized but Google Maps doesn't respond.

### Possible Causes & Solutions

#### 1. Chrome Not Running
**Check:** Did Selenium start Chrome?

**Solution:** Look for Chrome window with Google Maps. If missing:
- Check Python logs for Selenium errors
- Verify ChromeDriver is compatible with your Chrome version

#### 2. Handler Error
**Check:** Python logs show errors after "Executing XXXHandler"?

**Solution:**
- Read the error message
- Handler may need updating if Google Maps UI changed
- Check `gesture_handler.py` for the failing handler

#### 3. Selector Changed
**Check:** Error mentions "element not found"?

**Solution:** Google Maps UI may have changed. Update selectors in `maps_home_page.py`.

---

## 🔄 FusionEngine Not Routing Messages

### Problem
Gesture recognition sends messages but FusionEngine doesn't forward them.

### Check
Look at FusionEngine logs for:
```
MMI Lifecycle: mmi:ExtensionNotification; SOURCE: GESTURES; TARGET: FUSION
```

### Solution
1. Verify gesture recognition app is connected to FusionEngine
2. Check `fusion.scxml` has event handlers for GESTURES
3. Ensure gesture app is registered with correct source ID

---

## 🐍 Python Import Errors

### Problem
```
ModuleNotFoundError: No module named 'websockets'
```

### Solution
Install required packages:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install websockets selenium
```

---

## 🌐 Browser SSL Certificate Warning

### Problem
Browser shows "Your connection is not private" warning.

### Cause
The SSL certificate (`cert.pem`) is self-signed for local development.

### Solution
This is **normal** and **safe** for local development:
1. Click **"Advanced"**
2. Click **"Proceed to 127.0.0.1 (unsafe)"**

The connection is only on your local machine (localhost).

---

## 📊 Checking System Status

### Quick Health Check

Run these commands to verify each component:

**1. FusionEngine (Port 8000)**
```bash
curl -k https://127.0.0.1:8000
```
Should connect (may return error page, but connection works)

**2. WebApp HTTPS (Port 8082)**
```bash
curl -k https://127.0.0.1:8082
```
Should return HTML

**3. WebApp TTS WebSocket (Port 8083)**
```bash
# Check in browser console:
var ws = new WebSocket("ws://127.0.0.1:8083");
ws.onopen = () => console.log("Connected!");
```

**4. Python Assistant**
Check logs for:
```
INFO - Connected to MMI server
```

---

## 🔍 Debug Mode

### Enable Verbose Logging

In `main.py`, change logging level:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

This will show:
- All WebSocket messages
- Detailed Selenium actions
- TTS sending details

---

## 📞 Still Having Issues?

1. **Check all logs** - FusionEngine, WebApp, Assistant windows
2. **Run verification script:**
   ```bash
   cd Assistant
   python verify_gesture_mapping.py
   ```
3. **Test individual gestures:**
   ```bash
   python test_gestures.py --gesture camera
   ```
4. **Review system architecture** in [INTEGRATION_COMPLETE.md](INTEGRATION_COMPLETE.md)

---

## 🔧 Reset Everything

If things are completely broken:

1. **Close all terminals**
2. **Kill processes:**
   - Java (FusionEngine)
   - Python (server.py and main.py)
   - Chrome (if stuck)
3. **Restart in order:**
   - FusionEngine
   - WebApp
   - Assistant
4. **Verify each component** before starting the next

---

Last updated: 2025-12-18
