from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud import optimize_and_update_image
from src.model import SessionLocal


app = FastAPI()

# Datenbank-Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API-Endpunkt zur Optimierung eines Bildes
@app.post("/optimize/{post_id}", status_code=status.HTTP_200_OK)
def optimize_image(post_id: int, db: Session = Depends(get_db)):
    try:
        optimize_and_update_image(db, post_id)
        return {"message": "Bildoptimierung erfolgreich", "post_id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
