from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from src.websocket_client import send_update_to_server
import logging


app = FastAPI()

# Konfigurieren des Loggings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/trigger_update")
async def trigger_update(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(send_update_to_server)
        logger.info(f"### WEBSOCKET CLIENT API: Background Task für Websocket Client gestartet.")
        return {"message": "Update-Anfrage gesendet"}
    except:
        raise HTTPException(status_code=400, detail="Keine Comment-ID angegeben")




# from fastapi import FastAPI, HTTPException, BackgroundTasks
# from pydantic import BaseModel
# from src.websocket_client import send_update_to_server

# app = FastAPI()

# class UpdateRequest(BaseModel):
#     comment_id: int

# @app.post("/trigger_update")
# async def trigger_update(request: UpdateRequest, background_tasks: BackgroundTasks):
#     comment_id = request.comment_id
#     if comment_id:
#         background_tasks.add_task(send_update_to_server, comment_id)
#         return {"message": "Update-Anfrage gesendet"}
#     else:
#         raise HTTPException(status_code=400, detail="Keine Comment-ID angegeben")
