import asyncio
import websockets
import logging
import os


# Konfigurieren des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


WEBSOCKET_SERVER_HOST = os.getenv('WEBSOCKET_SERVER_HOST', 'localhost')
WEBSOCKET_PORT = os.getenv('WEBSOCKET_PORT', '8765')


async def send_update_to_frontend(comment_id):
    uri = f"ws://{WEBSOCKET_SERVER_HOST}:{WEBSOCKET_PORT}"  # Ersetzen Sie dies mit Ihrer WebSocket-Server-URL und dem Port
    async with websockets.connect(uri) as websocket:
        update_message = f"update_comment:{comment_id}"
        await websocket.send(update_message)
        response = await websocket.recv()
        logger.info(f"WebSocket Server Response: {response}")

def trigger_frontend_update(comment_id):
    asyncio.get_event_loop().run_until_complete(send_update_to_frontend(comment_id))


