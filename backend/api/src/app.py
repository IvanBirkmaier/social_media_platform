import backend.implementation.Database_Impl as database_impl
from fastapi import FastAPI
from backend.entity.Post import Post
from backend.entity.User import User

# Erstellen Sie eine Instanz der FastAPI-Anwendung
app = FastAPI()

# Definieren Sie eine Route, die auf GET-Anfragen unter "/begruesung" antwortet
@app.get("/begruesung/{username}/{email}")
def begruessung(username,email):
    # Create Users
    user1 = User(username=username, email=email)
    user1 = database_impl.add_user(user1)
    post1 = Post(image="image1.jpg", text="First post text", user_id=user1.id)
    database_impl.add_post(post1)
     # Get the latest post
    latest_post, post_user = database_impl.get_latest_post()
    if latest_post: 

        return {"user": str(post_user.username),
                "Email": str(post_user.email),
                "Timestamp": str(latest_post.timestamp)
                } 
    else:
        return{"No posts found."}
