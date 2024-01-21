from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.model import  SessionLocal
from src.crud import (create_post, delete_post, get_account_posts,get_post_full_image_by_id, get_random_posts_not_by_account)
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv() 
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')


# Fügt Middleware hinzu, um CORS für Ihre App zu konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    # allow_origins=["*"],  # Port auf dem frontend läuft oder dann halt oder ['*'] für alle Ursprünge
    allow_credentials=True,
    allow_methods=["*"],  # oder ['GET', 'POST', 'PUT', ...]
    allow_headers=["*"],
)

# Datenbank-Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PostCreate(BaseModel):
    account_id: int
    description: str
    base64_image: str

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_post_endpoint(post_create: PostCreate, db: Session = Depends(get_db)):
    post_id = create_post(db, post_create.account_id, post_create.description, post_create.base64_image)
    return {"post_id": post_id}

# Ändert den Rest-Call
@app.get("/posts/home/{account_id}")
def get_posts_by_user(account_id: int, db: Session = Depends(get_db)):
    posts = get_account_posts(db, account_id)
    return JSONResponse(content={"posts": posts}, status_code=status.HTTP_200_OK)


@app.get("/posts/{post_id}/image/")
def get_post_image(post_id: int, db: Session = Depends(get_db)):
    """
    Gibt das vollständige Bild eines Posts anhand seiner ID zurück.

    :param post_id: Die ID des Posts.
    :param db: Session-Objekt für die Datenbankverbindung.
    :return: Das vollständige Bild des Posts.
    """
    full_image_base64 = get_post_full_image_by_id(db, post_id)
    if full_image_base64  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post nicht gefunden")

    return JSONResponse(content={"full_image": full_image_base64 }, status_code=status.HTTP_200_OK)

@app.get("/posts/random/")
def get_random_posts(account_id: int, db: Session = Depends(get_db)):
    random_posts = get_random_posts_not_by_account(db, account_id)
    return JSONResponse(content={"posts": random_posts}, status_code=status.HTTP_200_OK)

@app.delete("/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_endpoint(post_id: int, db: Session = Depends(get_db)):
    # Optional: Check if the user is authorized to delete the post
    # This might involve checking if the user owns the post or has admin privileges
    try:
        delete_post(db, post_id)
        return JSONResponse(content={"detail": "Post successfully deleted"}, status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

