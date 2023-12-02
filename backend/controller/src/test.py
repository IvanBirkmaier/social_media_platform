from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Datenbank-Konfiguration
DATABASE_URL = "postgresql://user:password@localhost:5432/meine_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Datenbankmodell
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic-Modell für die Eingabedaten
class UserCreate(BaseModel):
    username: str
    email: str

# Methode zum Hinzufügen eines neuen Benutzers
def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username, email=user_create.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# FastAPI Endpunkt
@app.post("/users/", response_model=UserCreate)
def create_user_endpoint(user_create: UserCreate, db: Session = Depends(get_db)):
    # Prüfen, ob der Benutzer bereits existiert
    db_user = db.query(User).filter(User.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user_create)

# Hauptfunktion
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine) # Erstellen der Tabellen
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
