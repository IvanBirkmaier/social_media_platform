from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.model import SessionLocal
from src.crud import (create_comment, get_post_comments)

app = FastAPI()

class CommentCreate(BaseModel):
    account_id: int
    post_id: int
    text: str

# Datenbank-Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/comments/", response_model=CommentCreate, status_code=status.HTTP_201_CREATED)
def create_comment_endpoint(comment_create: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, comment_create.account_id, comment_create.post_id, comment_create.text)

@app.get("/posts/{post_id}/comments/")
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_comments(db, post_id)
