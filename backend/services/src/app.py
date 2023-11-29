import backend.implementation.Database_Impl as database_impl
from backend.entity.Post import Post
from backend.entity.User import User

# Das natürlich dann mit Frontend richtig anpassen!!!
# Bild muss noch richtig gespeichert werden, bisher nur Dummy String
# -> entweder dateipfad oder blob Ansatz
def main():
    # Create Database
    database_impl.create_tables()

    # Create Users
    user1 = User(username="User1", email="user1@example.com")
    user1 = database_impl.add_user(user1)

    user2 = User(username="User2", email="user2@example.com")
    user2 = database_impl.add_user(user2)

    user3 = User(username="User3", email="user3@example.com")
    user3 = database_impl.add_user(user3)

    # Create Posts
    post1 = Post(image="image1.jpg", text="First post text", user_id=user1.id)
    database_impl.add_post(post1)

    post2 = Post(image="image2.jpg", text="Second post text", user_id=user2.id)
    database_impl.add_post(post2)

    post3 = Post(image="image3.jpg", text="Third post text", user_id=user3.id)
    database_impl.add_post(post3)

    # Get the latest post
    latest_post, post_user = database_impl.get_latest_post()
    if latest_post:
        print(f"Latest Post:\nID: {latest_post.id}, Image: {latest_post.image}, Text: {latest_post.text}, "
              f"Timestamp: {latest_post.timestamp}, User: {post_user.username}, Email: {post_user.email}")
    else:
        print("No posts found.")


if __name__ == "__main__":
    main()
