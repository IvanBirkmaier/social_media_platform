from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.model import SessionLocal
from src.crud import (create_profile)
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

class ProfileCreate(BaseModel):
    account_id: int
    vorname: str
    nachname: str
    city: str
    plz: int
    street: str
    phone_number: str

# API-Endpunkt zum Erstellen eines Profils
@app.post("/profile/", response_model=ProfileCreate, status_code=status.HTTP_201_CREATED)
def create_profile_endpoint(profile_data: ProfileCreate, db: Session = Depends(get_db)):
    # Sie können hier zusätzliche Validierungen oder Geschäftslogiken hinzufügen
    profile = create_profile(db, **profile_data.dict())
    return profile
