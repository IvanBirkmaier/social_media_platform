from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.model import SessionLocal
from src.crud import (create_comment, get_post_comments)
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

class CommentCreate(BaseModel):
    account_id: int
    post_id: int
    text: str

@app.post("/comments/", response_model=CommentCreate, status_code=status.HTTP_201_CREATED)
def create_comment_endpoint(comment_create: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, comment_create.account_id, comment_create.post_id, comment_create.text)

@app.get("/posts/{post_id}/comments/")
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_comments(db, post_id)
