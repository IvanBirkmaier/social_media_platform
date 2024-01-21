from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.crud import classify_comments
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
@app.post("/classify/{comment_id}", status_code=status.HTTP_200_OK)
def classify_comment(comment_id: int, db: Session = Depends(get_db)):
    try:
        classify_comments(db, comment_id)
        return {"message": "Klassifizierung konnte erfolgreich umgesetzt werden", "post_id": comment_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))