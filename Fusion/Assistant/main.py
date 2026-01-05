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
	Extract intent, confidence, entities, and text from MMI message.
	Handles SPEECH, GESTURES, and FUSION modalities.

	Args:
		message: XML message from MMI server

	Returns:
		Tuple of (intent, confidence, entities, text)
	"""
	try:
		tags = ET.fromstring(message).findall('.//command')
		if not tags:
			return None, 0.0, {}, ""

		result = {}
		intent = None
		confidence = 1.0
		text = ""

		for tag in tags:
			command = json.loads(tag.text)
			recognized = command.get("recognized", [])

			if not recognized:
				continue

			command_type = recognized[0] if len(recognized) > 0 else None

			if command_type == "FUSION":
				# Extract fusion intent
				fusion_intent = recognized[1] if len(recognized) > 1 else None
				if fusion_intent:
					intent = fusion_intent

			elif command_type == "GESTURES":
				# Extract gesture type
				gesture_type = recognized[1] if len(recognized) > 1 else None
				if gesture_type:
					gesture_lower = gesture_type.lower()
					result["gesture"] = gesture_lower
					logger.info(f"Gesture recognized: {gesture_type} -> {gesture_lower}")

					# Map gesture semantic codes to intent names
					# Matches Gestures.xml <SEMANTIC> codes to Python handler intents
					gesture_to_intent = {
						# Confirmation gestures
						"thumbsup": "affirm",
						"thumbs_up": "affirm",
						"thumbup": "affirm",
						"yes": "affirm",
						"ok": "affirm",
						"thumbsdown": "deny",
						"thumbs_down": "deny",
						"thumbdown": "deny",
						"no": "deny",
						"cancel": "deny",

						# Gesture semantic codes from Gestures.xml
						"camera": "gesture_camera",           # Camera -> Coisas a fazer
						"downol": "gesture_down_option",     # DownOption_Left -> Down
						"enters": "gesture_enter_street",    # EnterStreet -> Enter Street View
						"exits": "gesture_exit_street",      # ExitStreet -> Exit Street View
						"hotels": "gesture_hotels",          # Hotels -> Hotels filter
						"restaurants": "gesture_restaurants", # Restaurants -> Restaurants filter
						"select": "gesture_select",          # Select -> Select item
						"swiped": "gesture_swipe_down",      # SwipeDown -> Swipe down
						"swipell": "gesture_swipe_left",     # SwipeLeft_Left -> Swipe left
						"swiperr": "gesture_swipe_right",    # SwipeRight_Right -> Swipe right
						"swipeu": "gesture_swipe_up",        # SwipeUp -> Swipe up
						"transports": "gesture_transports",  # Transports -> Transports filter
						"upor": "gesture_up_option",         # UpOption_Right -> Up
						"zoomi": "gesture_zoom_in",          # ZoomIn -> Zoom in
						"zoomo": "gesture_zoom_out",         # ZoomOut -> Zoom out
					}

					# If no intent set yet, use mapped intent or gesture as intent
					if not intent:
						intent = gesture_to_intent.get(gesture_lower, f"gesture_{gesture_lower}")
						logger.info(f"Mapped gesture '{gesture_lower}' to intent '{intent}'")

			elif command_type == "SPEECH":
				# Extract NLU data from speech
				nlu_data = command.get("nlu")
				if nlu_data:
					if isinstance(nlu_data, str):
						nlu_data = json.loads(nlu_data)

					# Get intent if not already set by FUSION
					if not intent:
						intent = nlu_data.get("intent", {}).get("name", "")
						confidence = nlu_data.get("intent", {}).get("confidence", 1.0)

					text = nlu_data.get("text", "")

					# Extract entities
					for entity in nlu_data.get("entities", []):
						entity_type = entity.get("entity")
						entity_value = entity.get("value")
						if entity_type and entity_value:
							result[entity_type] = entity_value

		return intent, confidence, result, text

	except Exception as e:
		logger.error(f"Error in nlu_extractor: {e}")
		return None, 0.0, {}, ""


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

			# Send welcome greeting
			await assistant.speak("Boas! Eu sou a Assistente de Google Maps. Como te posso ajudar?")
			logger.info("Sent welcome greeting")

			# Main loop: receive and process messages
			while True:
				try:
					message = await websocket.recv()
					if message is None or message in ["OK", "RENEW"]:
						continue

					# Log received message for debugging
					logger.debug(f"Received message: {message[:200]}...")

					# Skip TTS messages (messages with TARGET="SPEECHOUT")
					# These are our own TTS messages being echoed back
					if 'mmi:target="SPEECHOUT"' in message or 'target="SPEECHOUT"' in message:
						logger.debug("Skipping TTS message (TARGET=SPEECHOUT)")
						continue

					# Also skip startResponse messages (FusionEngine acknowledgments)
					if 'mmi:startResponse' in message or 'startResponse' in message:
						logger.debug("Skipping startResponse message")
						continue

					# Extract intent from message
					intent, confidence, entities, text = nlu_extractor(message)

					if not intent:
						logger.warning("No intent extracted from message")
						continue

					logger.info(
						f"Received - Intent: {intent}, "
						f"Confidence: {confidence:.2f}, "
						f"Entities: {entities}, "
						f"Text: '{text}'"
					)

					# Handle intent with assistant
					response_message = assistant.handle_intent(
						intent=intent,
						confidence=confidence,
						entities=entities,
						metadata={"text": text}
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
