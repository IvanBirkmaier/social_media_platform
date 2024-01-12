from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from src.model import Account, SessionLocal
from src.crud import (create_account, check_account_login, delete_account, check_username_existence, check_email_existence, get_account_id_by_username)

app = FastAPI()

# Datenbank-Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# API Endpunkte
@app.post("/account/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_create: AccountCreate, db: Session = Depends(get_db)):
    db_user = db.query(Account).filter(Account.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_account(db, user_create.username, user_create.email, user_create.password)

@app.get("/account-id/{username}")
def get_account_id(username: str, db: Session = Depends(get_db)):
    account_id = get_account_id_by_username(db, username)
    if account_id is not None:
        return {"account_id": account_id}
    else:
        return {"account_id": 0}

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
    return {"id": user.id, "username": user.username}

@app.delete("/account/{account_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_account_endpoint(account_id: int, db: Session = Depends(get_db)):
    # Optional: Fügen Sie hier Authentifizierungs- und Autorisierungslogiken hinzu.
    # Beispiel: Überprüfen Sie, ob der eingeloggte Benutzer das Recht hat, diesen Account zu löschen.
    try:
        delete_account(db, account_id)
        return JSONResponse(content={"detail": "Account successfully deleted"}, status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
