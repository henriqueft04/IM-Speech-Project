import http.server
import ssl
import asyncio
import websockets
import json
import threading

# Configurações do servidor
server_address = ('', 8082)  # Porta 8082 para HTTPS
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Configuração SSL (compatible with Python 3.10 and 3.12)
try:
    # Python 3.12+ approach
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
except AttributeError:
    # Python 3.10 approach (deprecated but still works)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile='cert.pem',
                                   keyfile='key.pem',
                                   ssl_version=ssl.PROTOCOL_TLS)

print("Servidor HTTPS na porta 8082...")

# WebSocket server for TTS on port 8083
connected_clients = set()

async def tts_handler(websocket, path):
    """Handle WebSocket connections for TTS"""
    print(f"TTS WebSocket client connected from {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast received TTS message to all connected clients
            print(f"Received TTS message: {message}")
            disconnected = set()
            for client in connected_clients:
                try:
                    await client.send(message)
                except:
                    disconnected.add(client)
            connected_clients.difference_update(disconnected)
    except websockets.exceptions.ConnectionClosed:
        print("TTS WebSocket client disconnected")
    finally:
        connected_clients.discard(websocket)

async def start_websocket_server():
    """Start WebSocket server on port 8083"""
    async with websockets.serve(tts_handler, "127.0.0.1", 8083):
        print("TTS WebSocket server running on ws://127.0.0.1:8083")
        await asyncio.Future()  # run forever

def run_websocket_server():
    """Run WebSocket server in asyncio event loop"""
    asyncio.run(start_websocket_server())

# Start WebSocket server in a separate thread
ws_thread = threading.Thread(target=run_websocket_server, daemon=True)
ws_thread.start()

# Start HTTPS server (blocks)
httpd.serve_forever()
