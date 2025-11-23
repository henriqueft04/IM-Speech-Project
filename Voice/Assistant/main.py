"""
Main entry point for the Google Maps Voice Assistant.
Connects to MMI server via WebSocket and processes voice commands.
"""

import sys
from pathlib import Path

# Add the Assistant directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

import asyncio
import websockets
import json
import xml.etree.ElementTree as ET
import ssl
import logging

# Import assistant components
from config import DriverManager
from application.assistant import GoogleMapsAssistant
from application.services import TTSService
from config.settings import MMI_URL, LOG_LEVEL, LOG_FORMAT, CHROME_PROFILE_PATH

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def nlu_extractor(message):
	"""
	Extract intent, confidence, and entities from MMI message.

	Args:
		message: XML message from MMI server

	Returns:
		Tuple of (intent, confidence, entities)
	"""
	tags = ET.fromstring(message).findall('.//command')
	message = json.loads(tags.pop(0).text)
	modality = message["recognized"][0]

	if modality == "SPEECH":
		nlu_data = json.loads(message["nlu"])
		intent = nlu_data.get("intent", {}).get("name", "")
		confidence = nlu_data.get("intent", {}).get("confidence", 1.0)
		result = {}

		for entity in nlu_data.get("entities", []):
			result[entity["entity"]] = entity["value"]

		return intent, confidence, result

	return None, 0.0, {}


def ignore_ssl():
	"""
	Create SSL context that ignores certificate verification.

	Returns:
		SSL context
	"""
	ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
	ssl_context.check_hostname = False
	ssl_context.verify_mode = ssl.CERT_NONE

	return ssl_context


async def main():
	"""
	Main async function that runs the voice assistant.
	"""
	mmi_url = MMI_URL
	ssl_context = ignore_ssl()

	# Initialize WebDriver and Assistant (once, persistent session)
	logger.info("Initializing Google Maps Assistant...")
	driver_manager = DriverManager()

	try:
		# Start driver
		driver = driver_manager.start(
			headless=False,
			user_data_dir=CHROME_PROFILE_PATH
		)

		# Initialize TTS service
		tts_service = TTSService()

		# Initialize assistant
		assistant = GoogleMapsAssistant(driver, tts_service)

		logger.info("Assistant initialized successfully")
		logger.info(f"Connecting to MMI server at {mmi_url}...")

		# Connect to WebSocket
		async with websockets.connect(mmi_url, ssl=ssl_context) as websocket:
			logger.info("Connected to MMI server")

			# Set WebSocket for TTS service
			assistant.set_tts_websocket(websocket)

			# Main loop: receive and process messages
			while True:
				try:
					message = await websocket.recv()
					if message is None or message in ["OK", "RENEW"]:
						continue

					# Extract intent from message
					intent, confidence, entities = nlu_extractor(message)

					if not intent:
						logger.warning("No intent extracted from message")
						continue

					logger.info(
						f"Received - Intent: {intent}, "
						f"Confidence: {confidence:.2f}, "
						f"Entities: {entities}"
					)

					# Handle intent with assistant
					response_message = assistant.handle_intent(
						intent=intent,
						confidence=confidence,
						entities=entities
					)

					# Send response back via TTS
					if response_message:
						logger.info(f"Response: {response_message}")
						await assistant.speak(response_message)

				except websockets.exceptions.ConnectionClosed:
					logger.error("WebSocket connection closed")
					break

				except Exception as e:
					logger.error(f"Error processing message: {e}", exc_info=True)
					# Try to send error message to user
					try:
						await assistant.speak("Desculpa, ocorreu um erro")
					except:
						pass

	except KeyboardInterrupt:
		logger.info("Shutting down due to keyboard interrupt")

	except Exception as e:
		logger.error(f"Fatal error: {e}", exc_info=True)

	finally:
		# Clean up
		logger.info("Cleaning up...")
		if 'assistant' in locals():
			assistant.shutdown()
		if 'driver_manager' in locals():
			driver_manager.stop()
		logger.info("Shutdown complete")


if __name__ == "__main__":
	asyncio.run(main())
