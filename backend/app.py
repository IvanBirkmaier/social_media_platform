from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from services.src.model import User, SessionLocal, init_db
from services.src.crud import (create_user, check_user_login, create_post,
                               create_comment, get_user_posts, get_post_comments,
                               get_user_id_by_username, get_random_posts_not_by_user)

app = FastAPI()

# Pydantic Modelle
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    user_id: int
    description: str
    base64_image: str

class CommentCreate(BaseModel):
    user_id: int
    post_id: int
    text: str

# Datenbank-Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpunkte
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_create: UserCreate, db: Session = Depends(get_db)):
    init_db()  # Initialisieren der Datenbank
    db_user = db.query(User).filter(User.username == user_create.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user_create.username, user_create.email, user_create.password)

@app.post("/login/")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = check_user_login(db, user_login.username, user_login.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"message": "Login successful"}

@app.post("/posts/", response_model=PostCreate, status_code=status.HTTP_201_CREATED)
def create_post_endpoint(post_create: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post_create.user_id, post_create.description, post_create.base64_image)

@app.post("/comments/", response_model=CommentCreate, status_code=status.HTTP_201_CREATED)
def create_comment_endpoint(comment_create: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db, comment_create.user_id, comment_create.post_id, comment_create.text)

@app.get("/users/{user_id}/posts/")
def get_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_posts(db, user_id)

@app.get("/posts/{post_id}/comments/")
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_comments(db, post_id)

@app.get("/users/username/{username}/")
def get_userid_by_username(username: str, db: Session = Depends(get_db)):
    return get_user_id_by_username(db, username)

@app.get("/posts/random/")
def get_random_posts(user_id: int, db: Session = Depends(get_db)):
    return get_random_posts_not_by_user(db, user_id)
