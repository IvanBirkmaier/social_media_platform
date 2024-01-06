from sqlalchemy.orm import Session
from sqlalchemy import func
from .model import Account, Profile, Post, Comment
import bcrypt
import base64


# Passwort in einen Hash machen
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Passwort mit dem Hash vergleichen
def check_password_hash(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))


# Erstellen eines Accounts (Registrierung)
def create_account(db: Session, username: str, email: str, password: str):
    hashed_password = hash_password(password)
    account = Account(username=username, email=email, password_hash=hashed_password)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

# Erstellen eines Profils
def create_profile(db: Session, account_id: int, vorname: str, nachname: str, city: str, plz: int, street: str, phone_number: str):
    profile = Profile(account_id=account_id, vorname=vorname, nachname=nachname, city=city, plz=plz, street=street, phone_number=phone_number)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

# Lesen eines Profils über die Account-ID
def read_profile(db: Session, account_id: int):
    return db.query(Profile).filter(Profile.account_id == account_id).first()


# Überprüfen, ob der Benutzername bereits vergeben ist
def check_username_existence(db: Session, username: str):
    return db.query(Account).filter(Account.username == username).first() is not None

# Überprüfen, ob die E-Mail bereits vergeben ist
def check_email_existence(db: Session, email: str):
    return db.query(Account).filter(Account.email == email).first() is not None


# User Login
def check_account_login(db: Session, username: str, password: str):
    account = db.query(Account).filter(Account.username == username).first()
    if account and check_password_hash(password, account.password_hash):
        return account
    return None

# Funktion, um Bytes in einen Base64-String zu konvertieren
def convert_bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# Post zu erstellen
def create_post(db: Session, account_id: int, description: str, base64_image: str):
    image_bytes = base64.b64decode(base64_image)
    db_post = Post(account_id=account_id, description=description, image=image_bytes)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Konvertieren Sie das Bild in Base64, bevor Sie das Objekt zurückgeben
    # db_post.image = convert_bytes_to_base64(db_post.image)
    db_post.base64_image = base64_image

    return db_post

# Erstellen eines Kommentars
def create_comment(db: Session, account_id: int, post_id: int, text: str):
    db_comment = Comment(account_id=account_id, post_id=post_id, text=text)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Hilfsfunktion, um Bytes in einen Base64-String zu konvertieren
def convert_image_to_base64(image_bytes):
    if image_bytes:
        return base64.b64encode(image_bytes).decode('utf-8')
    return None

# Funktion, um die Account-ID anhand des Benutzernamens zu finden
def get_account_id_by_username(db: Session, username: str):
    account = db.query(Account).filter(Account.username == username).first()
    if account:
        return account.id
    else:
        return None

# CRUD-Methode zum Abrufen der Posts eines Benutzers
# def get_account_posts(db: Session, account_id: int):
#     posts = db.query(Post).filter(Post.account_id == account_id).all()
#     for post in posts:
#         # Konvertieren Sie das Bild in Base64, bevor Sie das Objekt zurückgeben
#         post.image = convert_image_to_base64(post.image)
#     return posts

def get_account_posts(db: Session, account_id: int):
    posts = db.query(Post, Account.username).join(Account).filter(Post.account_id == account_id).all()
    return [{
        "id": post.id,
        "account_id": post.account_id,
        "description": post.description,
        "base64_image": convert_image_to_base64(post.image),
        "username": username
    } for post, username in posts]


# Auslesen aller Comments eines Posts
# def get_post_comments(db: Session, post_id: int):
#     return db.query(Comment).filter(Comment.post_id == post_id).all()
def get_post_comments(db: Session, post_id: int):
    return (
        db.query(Comment, Account.username)
        .join(Account, Comment.account_id == Account.id)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())  # Sortiert nach Erstellungsdatum, neueste zuerst
        .all()
    )


# Auslesen von 9 zufälligen Post die nicht dem User gehören (Für ein Feed)
def get_random_posts_not_by_account(db: Session, account_id: int):
    posts = db.query(Post, Account.username).join(Account, Post.account_id == Account.id).filter(Post.account_id != account_id).order_by(func.random()).limit(9).all()
    return [{
        "id": post.id,
        "account_id": post.account_id,
        "description": post.description,
        "base64_image": convert_image_to_base64(post.image),
        "username": username
    } for post, username  in posts]


# Löscht einen Post
def delete_post(db: Session, post_id: int):
    # Suche den Post in der Datenbank über seine ID
    db_post = db.query(Post).filter(Post.id == post_id).first()

    # Überprüfe, ob der Post existiert
    if db_post is None:
        raise ValueError("Post mit der ID {} wurde nicht gefunden.".format(post_id))

    # Lösche den Post aus der Datenbank
    db.delete(db_post)
    db.commit()


