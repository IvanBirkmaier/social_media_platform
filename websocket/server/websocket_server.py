import asyncio
import websockets
import json
import os


# Laden der Umgebungsvariablen
WEBSOCKET_SERVER_HOST = os.getenv('WEBSOCKET_SERVER_HOST', "0.0.0.0")
WEBSOCKET_SERVER_PORT = os.getenv('WEBSOCKET_SERVER_PORT', 8765)

connected_clients = set()

async def register(websocket):
    connected_clients.add(websocket)

async def unregister(websocket):
    connected_clients.remove(websocket)

async def echo(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'forward':
                # Hier könnten Sie eine spezifische Logik implementieren, um die Nachricht zu bearbeiten
                forward_message = json.dumps({"action": "update", "content": data['content']})
                await asyncio.wait([client.send(forward_message) for client in connected_clients])
    finally:
        await unregister(websocket)

start_server = websockets.serve(echo, WEBSOCKET_SERVER_HOST, WEBSOCKET_SERVER_PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
