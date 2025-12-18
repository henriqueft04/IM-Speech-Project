@echo off
title Starting Gesture System
echo ========================================
echo Starting Gesture Recognition System
echo ========================================
echo.
echo IMPORTANT: This will start 3 components:
echo   1. FusionEngine (MMI message router)
echo   2. WebApp TTS Server (audio output)
echo   3. Python Assistant (Google Maps control)
echo.
echo Wait for each to fully start before continuing...
echo.
pause

echo.
echo [1/3] Starting FusionEngine...
echo ----------------------------------------
echo Wait for "Websocket Server is running" message
echo.
start "FusionEngine" cmd /k "cd /d "%~dp0FusionEngine" && start.bat"
echo.
echo Press any key AFTER you see FusionEngine is running...
pause > nul

echo.
echo [2/3] Starting WebApp TTS Server...
echo ----------------------------------------
echo Wait for "TTS WebSocket server running" message
echo.
start "WebApp TTS" cmd /k "cd /d "%~dp0WebAppAssistantV2" && python server.py"
echo.
echo Press any key AFTER you see WebSocket server running...
pause > nul

echo.
echo [3/3] Starting Python Assistant...
echo ----------------------------------------
echo Wait for "Connected to MMI server" message
echo.
start "Python Assistant" cmd /k "cd /d "%~dp0Assistant" && python main.py"
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo All components started!
echo ========================================
echo.
echo NEXT STEPS:
echo.
echo 1. Open your browser to:
echo    https://127.0.0.1:8082/index.htm
echo.
echo 2. Accept the SSL certificate warning
echo    (Click "Advanced" then "Proceed to 127.0.0.1")
echo.
echo 3. Verify browser console shows:
echo    "TTS WebSocket connected"
echo.
echo 4. Start your gesture recognition application
echo.
echo 5. Make gestures and enjoy!
echo.
echo Press any key to close this launcher...
pause > nul
