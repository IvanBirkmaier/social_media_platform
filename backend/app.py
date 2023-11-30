import services.src.implementation.Database_Impl as Database_Impl
from services.src.entity.Post import Post
from services.src.entity.User import User
from fastapi import FastAPI


# Erstellen Sie eine Instanz der FastAPI-Anwendung
app = FastAPI()

# Definieren Sie eine Route, die auf GET-Anfragen unter "/begruesung" antwortet
@app.get("/begruesung/{username}/{email}")
def begruessung(username,email):
    # Create Users
    user1 = User(username=username, email=email)
    user1 = Database_Impl.add_user(user1)
    post1 = Post(image="image1.jpg", text="First post text", user_id=user1.id)
    Database_Impl.add_post(post1)
     # Get the latest post
    latest_post, post_user = Database_Impl.get_latest_post()
    if latest_post: 

        return {"user": str(post_user.username),
                "Email": str(post_user.email),
                "Timestamp": str(latest_post.timestamp)
                } 
    else:
        return{"No posts found."}
