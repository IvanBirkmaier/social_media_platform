from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading
import asyncio
from src.websocket_client import send_update_to_frontend  
import websockets
import logging
import os

app = FastAPI()

API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = os.getenv('API_PORT', 8003)



class UpdateRequest(BaseModel):
    comment_id: int

@app.post("/trigger_update")
async def trigger_update(request: UpdateRequest):
    comment_id = request.comment_id
    if comment_id:
        await send_update_to_frontend(comment_id)
        return {"message": "Update-Anfrage gesendet"}
    raise HTTPException(status_code=400, detail="Keine Comment-ID angegeben")

def run_fastapi():
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)  

def run_websocket_client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    threading.Thread(target=run_fastapi).start()
    threading.Thread(target=run_websocket_client).start()
