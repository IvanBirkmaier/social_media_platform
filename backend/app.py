from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from services.src.model import Account, SessionLocal, Base, engine
from dotenv import load_dotenv
import os
from services.src.crud import (create_profile, create_account, check_account_login, create_post,
                               create_comment, get_account_posts, get_post_comments,
                               get_random_posts_not_by_account, check_username_existence, check_email_existence)

load_dotenv() 
FRONTEND_URL = os.environ.get("FRONTEND_URL") # Für die Connection zum Frontend (Sicherheitsmaßnahme)

def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()

app = FastAPI()

# Fügt Middleware hinzu, um CORS für Ihre App zu konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
   # allow_origins=["*"],  # Port auf dem frontend läuft oder dann halt oder ['*'] für alle Ursprünge
    allow_credentials=True,
    allow_methods=["*"],  # oder ['GET', 'POST', 'PUT', ...]
    allow_headers=["*"],
)

class AccountCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class AccountResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    account_id: int
    description: str
    base64_image: str

class CommentCreate(BaseModel):
    account_id: int
    post_id: int
    text: str

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

# API Endpunkte
@app.post("/account/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_create: AccountCreate, db: Session = Depends(get_db)):
    db_user = db.query(Account).filter(Account.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_account(db, user_create.username, user_create.email, user_create.password)

# API-Endpunkt zum Erstellen eines Profils
@app.post("/profile/", response_model=ProfileCreate, status_code=status.HTTP_201_CREATED)
def create_profile_endpoint(profile_data: ProfileCreate, db: Session = Depends(get_db)):
    # Sie können hier zusätzliche Validierungen oder Geschäftslogiken hinzufügen
    profile = create_profile(db, **profile_data.dict())
    return profile

@app.get("/check-username/{username}")
def check_username(username: str, db: Session = Depends(get_db)):
    if check_username_existence(db, username):
        return JSONResponse(content={"username_exists": True}, status_code=200)
    return JSONResponse(content={"username_exists": False}, status_code=200)

@app.get("/check-email/{email}")
def check_email(email: str, db: Session = Depends(get_db)):
    if check_email_existence(db, email):
        return JSONResponse(content={"email_exists": True}, status_code=200)
    return JSONResponse(content={"email_exists": False}, status_code=200)

@app.post("/login/")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = check_account_login(db, user_login.username, user_login.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Falscher Benutzername oder Passwort")
    return {"message": "Login successful"}

@app.post("/posts/", response_model=PostCreate, status_code=status.HTTP_201_CREATED)
def create_post_endpoint(post_create: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post_create.account_id, post_create.description, post_create.base64_image)

@app.post("/comments/", response_model=CommentCreate, status_code=status.HTTP_201_CREATED)
def create_comment_endpoint(comment_create: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, comment_create.account_id, comment_create.post_id, comment_create.text)

@app.get("/account/{account_id}/posts/")
def get_posts_by_user(account_id: int, db: Session = Depends(get_db)):
    return get_account_posts(db, account_id)

@app.get("/posts/{post_id}/comments/")
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_comments(db, post_id)

@app.get("/posts/random/")
def get_random_posts(account_id: int, db: Session = Depends(get_db)):
    return get_random_posts_not_by_account(db, account_id)
