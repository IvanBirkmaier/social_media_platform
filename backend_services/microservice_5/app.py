from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.model import SessionLocal
from src.crud import (create_profile)

app = FastAPI()

class ProfileCreate(BaseModel):
    account_id: int
    vorname: str
    nachname: str
    city: str
    plz: int
    street: str
    phone_number: str

# Datenbank-Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API-Endpunkt zum Erstellen eines Profils
@app.post("/profile/", response_model=ProfileCreate, status_code=status.HTTP_201_CREATED)
def create_profile_endpoint(profile_data: ProfileCreate, db: Session = Depends(get_db)):
    # Sie können hier zusätzliche Validierungen oder Geschäftslogiken hinzufügen
    profile = create_profile(db, **profile_data.dict())
    return profile
