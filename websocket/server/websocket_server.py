import asyncio
import websockets
import os
import logging
import json

# Konfigurieren des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Laden der Umgebungsvariablen
WEBSOCKET_SERVER_HOST = os.getenv('WEBSOCKET_SERVER_HOST', "0.0.0.0")
WEBSOCKET_SERVER_PORT = int(os.getenv('WEBSOCKET_SERVER_PORT', 8765))

connected_clients = set()

async def register(websocket):
    logger.info("### WEBSOCKET SERVER: WebSocket-Client registriert")
    connected_clients.add(websocket)

async def unregister(websocket):
    logger.info("### WEBSOCKET SERVER: WebSocket-Client nicht mehr registriert")
    connected_clients.remove(websocket)

async def echo(websocket, path):
    logger.info("### WEBSOCKET SERVER: WebSocket-Server aktiv")
    await register(websocket)
    try:
        async for _ in websocket:
            logger.info("### WEBSOCKET SERVER: Signal von Client bekommen")
            signal = json.dumps({"action": "update"})
            await asyncio.wait([client.send(signal) for client in connected_clients])
            logger.info("### WEBSOCKET SERVER: Signal an alle Clients gesendet")
    finally:
        await unregister(websocket)

start_server = websockets.serve(echo, WEBSOCKET_SERVER_HOST, WEBSOCKET_SERVER_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

