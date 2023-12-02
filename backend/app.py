from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.src.model import User, SessionLocal, init_db
from services.src.crud import create_user

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    email: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserCreate)
def create_user_endpoint(user_create: UserCreate, db: Session = Depends(get_db)):
    init_db() # Initialisieren der Datenbank
    db_user = db.query(User).filter(User.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user_create.username, user_create.email)

