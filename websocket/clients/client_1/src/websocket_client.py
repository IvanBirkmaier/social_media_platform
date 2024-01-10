import asyncio
import websockets
import os
import json
import logging



# Konfigurieren des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


WEBSOCKET_SERVER_HOST = os.getenv('WEBSOCKET_SERVER_HOST', 'websocket_server')

WEBSOCKET_PORT = int(os.getenv('WEBSOCKET_PORT', 8765))


async def send_update_to_server(comment_id):
    uri = f"ws://{WEBSOCKET_SERVER_HOST}:{WEBSOCKET_PORT}"
    async with websockets.connect(uri) as websocket:
        logger.info(f"################################## MESSSAGE SENDED TO WebSocket Server Response")
        update_message = json.dumps({"type": "update_comment", "comment_id": comment_id})
        await websocket.send(update_message)
        response = await websocket.recv()
        logger.info(f"WebSocket Server Response: {response}")


def trigger_server_update(comment_id):
    asyncio.get_event_loop().run_until_complete(send_update_to_server(comment_id))



