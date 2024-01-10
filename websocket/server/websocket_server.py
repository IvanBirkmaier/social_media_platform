import asyncio
import websockets
import json
import os
import logging



# Konfigurieren des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Laden der Umgebungsvariablen
WEBSOCKET_SERVER_HOST = os.getenv('WEBSOCKET_SERVER_HOST', "0.0.0.0")
WEBSOCKET_SERVER_PORT = int(os.getenv('WEBSOCKET_SERVER_PORT', 8765))

connected_clients = set()

async def register(websocket):
    logger.info(f"################################## WEBSOCKET CLIENT REGISTRIERT")
    connected_clients.add(websocket)

async def unregister(websocket):
    logger.info(f"################################## WEBSOCKET CLIENT NICHT MEHR REGISTRIERT")
    connected_clients.remove(websocket)

async def echo(websocket, path):
    logger.info(f"################################## WEBSOCKET SERVER HEY")
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'forward':
                # Hier könnten Sie eine spezifische Logik implementieren, um die Nachricht zu bearbeiten
                forward_message = json.dumps({"action": "update", "content": data['content']})
                await asyncio.wait([client.send(forward_message) for client in connected_clients])
                logger.info(f"################################## WEBSOCKET SERVER HEY")
    finally:
        await unregister(websocket)

start_server = websockets.serve(echo, WEBSOCKET_SERVER_HOST, WEBSOCKET_SERVER_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



# import asyncio
# import websockets
# import os
# import logging

# # Konfigurieren des Loggings
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Laden der Umgebungsvariablen
# WEBSOCKET_SERVER_HOST = os.getenv('WEBSOCKET_SERVER_HOST', "0.0.0.0")
# WEBSOCKET_SERVER_PORT = int(os.getenv('WEBSOCKET_SERVER_PORT', 8765))

# connected_clients = set()

# async def register(websocket):
#     logger.info("WebSocket-Client registriert")
#     connected_clients.add(websocket)

# async def unregister(websocket):
#     logger.info("WebSocket-Client nicht mehr registriert")
#     connected_clients.remove(websocket)

# async def echo(websocket, path):
#     logger.info("WebSocket-Server aktiv")
#     await register(websocket)
#     try:
#         async for _ in websocket:
#             signal = json.dumps({"action": "update"})
#             await asyncio.wait([client.send(signal) for client in connected_clients])
#             logger.info("Signal an alle Clients gesendet")
#     finally:
#         await unregister(websocket)

# start_server = websockets.serve(echo, WEBSOCKET_SERVER_HOST, WEBSOCKET_SERVER_PORT)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
