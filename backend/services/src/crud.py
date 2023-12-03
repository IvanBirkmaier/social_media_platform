from sqlalchemy.orm import Session
from sqlalchemy import func
from .model import User,Post,Comment
import bcrypt

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


# Einen Post erstellen
def create_post(db: Session, user_id: int, description: str, image: bytes):
    db_post = Post(user_id=user_id, description=description, image=image)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Erstellen eines Kommentars
def create_comment(db: Session, user_id: int, post_id: int, text: str):
    db_comment = Comment(user_id=user_id, post_id=post_id, text=text)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Auslesen aller Post eines Users
def get_user_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).all()

# Auslesen aller Comments eines Posts
def get_post_comments(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()

# Auslesen der UserID über den Username
def get_user_id_by_username(db: Session, username: str):
    return db.query(User.id).filter(User.username == username).all()

# Auslesen von 10 zufälligen Post die nicht dem User gehören (Für ein Feed)
def get_random_posts_not_by_user(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id != user_id).order_by(func.random()).limit(10).all()



