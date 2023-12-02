# import services.src.implementation.Database_Impl as Database_Impl
# from services.src.entity.Post import Post
# from services.src.entity.User import User
# import controller.src.test as test
# #from fastapi import FastAPI
# from fastapi import FastAPI, Depends, HTTPException



# # Erstellen Sie eine Instanz der FastAPI-Anwendung
# app = FastAPI()

# # # Definieren Sie eine Route, die auf GET-Anfragen unter "/begruesung" antwortet
# # @app.get("/sqlite/{username}/{email}")
# # def sqlite(username,email):
# #     # Create Users
# #     user1 = User(username=username, email=email)
# #     user1 = Database_Impl.add_user(user1)
# #     post1 = Post(image="image1.jpg", text="First post text", user_id=user1.id)
# #     Database_Impl.add_post(post1)
# #      # Get the latest post
# #     latest_post, post_user = Database_Impl.get_latest_post()
# #     if latest_post: 

# #         return {"user": str(post_user.username),
# #                 "Email": str(post_user.email),
# #                 "Timestamp": str(latest_post.timestamp)
# #                 } 
# #     else:
# #         return{"No posts found."}

# # Definieren Sie eine Route, die auf GET-Anfragen unter "/begruesung" antwortet

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from controller.src.model import User, SessionLocal, init_db
from controller.src.crud import create_user

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

