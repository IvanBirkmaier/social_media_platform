from sqlalchemy.orm import Session
from sqlalchemy import func
from .model import User,Post,Comment
import bcrypt
import base64


# Passwort in einen Hash machen
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Passwort mit dem Hash vergleichen
def check_password_hash(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))


# Erstellen eines Users (registrierung)
def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = hash_password(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# User Login
def check_user_login(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and check_password_hash(password, user.password_hash):
        return user
    return None

# Funktion, um Bytes in einen Base64-String zu konvertieren
def convert_bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# Post zu erstellen
def create_post(db: Session, user_id: int, description: str, base64_image: str):
    image_bytes = base64.b64decode(base64_image)
    db_post = Post(user_id=user_id, description=description, image=image_bytes)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Konvertieren Sie das Bild in Base64, bevor Sie das Objekt zurückgeben
    # db_post.image = convert_bytes_to_base64(db_post.image)
    db_post.base64_image = base64_image

    return db_post

# Erstellen eines Kommentars
def create_comment(db: Session, user_id: int, post_id: int, text: str):
    db_comment = Comment(user_id=user_id, post_id=post_id, text=text)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Hilfsfunktion, um Bytes in einen Base64-String zu konvertieren
def convert_image_to_base64(image_bytes):
    if image_bytes:
        return base64.b64encode(image_bytes).decode('utf-8')
    return None

# CRUD-Methode zum Abrufen der Posts eines Benutzers
def get_user_posts(db: Session, user_id: int):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    for post in posts:
        # Konvertieren Sie das Bild in Base64, bevor Sie das Objekt zurückgeben
        post.image = convert_image_to_base64(post.image)
    return posts

# Auslesen aller Comments eines Posts
def get_post_comments(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

# Auslesen der UserID über den Username
def get_user_id_by_username(db: Session, username: str):
    result = db.query(User.id).filter(User.username == username).all()
    # Extrahieren Sie die IDs aus den Tupeln und geben Sie sie als Liste zurück
    return [user_id for (user_id,) in result]


# Auslesen von 10 zufälligen Post die nicht dem User gehören (Für ein Feed)
def get_random_posts_not_by_user(db: Session, user_id: int):
    posts = db.query(Post).filter(Post.user_id != user_id).order_by(func.random()).limit(10).all()
    for post in posts:
        # Konvertieren Sie das Bild in Base64, bevor Sie das Objekt zurückgeben
        post.image = convert_image_to_base64(post.image)
    return posts



