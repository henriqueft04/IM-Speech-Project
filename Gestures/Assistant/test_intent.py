"""
Simple test script to verify the assistant is working.
Tests intent handling without requiring the web interface.
"""

import sys
from pathlib import Path

# Add the Assistant directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from application.assistant import GoogleMapsAssistant
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application.services import TTSService

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com/maps")

# Create assistant
tts_service = TTSService()
assistant = GoogleMapsAssistant(driver, tts_service)

print("\n" + "="*60)
print("GOOGLE MAPS ASSISTANT TEST")
print("="*60)

# Test 1: Greet
print("\n[TEST 1] Testing greet intent...")
response = assistant.handle_intent("greet", 0.95, {})
print(f"Response: {response}")

# Test 2: Search location
print("\n[TEST 2] Testing search_location intent...")
response = assistant.handle_intent("search_location", 0.95, {"location": "Lisboa"})
print(f"Response: {response}")

# Test 3: Zoom in
print("\n[TEST 3] Testing zoom_in intent...")
response = assistant.handle_intent("zoom_in", 0.95, {})
print(f"Response: {response}")

# Test 4: Thanks
print("\n[TEST 4] Testing thanks intent...")
response = assistant.handle_intent("thanks", 0.95, {})
print(f"Response: {response}")

print("\n" + "="*60)
print("Tests complete! Check the Google Maps window.")
print("="*60)

input("\nPress Enter to close...")
driver.quit()
