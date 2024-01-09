from sqlalchemy.orm import Session
from sqlalchemy import func
from .model import Account, Profile, Post, Comment
from .producer import kafka_send_post_id, kafka_send_comment_id
import bcrypt
import base64
from PIL import Image
import io
from mimetypes import guess_extension, guess_type
from io import BytesIO


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


def validate_image_bytes(image_bytes):
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            # Optional: Weitere Überprüfungen hinzufügen (z.B. Bildgröße, Format)
            pass
    except IOError:
        raise ValueError("Ungültiges Bildformat oder beschädigte Bilddaten")


# Post zu erstellen
def create_post(db: Session, account_id: int, description: str, base64_image: str):
    
    # Dekodierung des Base64-Strings in Bytes
    if "," in base64_image:
        base64_image = base64_image.split(',')[1]
    image_bytes = base64.b64decode(base64_image)

    # Validierung der Bildbytes
    validate_image_bytes(image_bytes)
    db_post = Post(account_id=account_id, description=description, full_image=image_bytes)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    # db_post.base64_image = base64_image
    kafka_send_post_id(db_post.id)
    print(" 9### kafka send")
    return db_post


# Erstellen eines Kommentars
def create_comment(db: Session, account_id: int, post_id: int, text: str):
    db_comment = Comment(account_id=account_id, post_id=post_id, text=text)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # Senden der Kommentar-ID an Kafka
    kafka_send_comment_id(db_comment.id)
    return db_comment


def convert_image_to_base64(image_bytes):
    if image_bytes:
        image_stream = BytesIO(image_bytes)
        image_format = Image.open(image_stream).format.lower()
        mime_type, _ = guess_type(f".{image_format}")
        base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:{mime_type};base64,{base64_encoded}"
    return None



# Funktion, um die Account-ID anhand des Benutzernamens zu finden
def get_account_id_by_username(db: Session, username: str):
    account = db.query(Account).filter(Account.username == username).first()
    if account:
        return account.id
    else:
        return None

# CRUD-Methode zum Abrufen der Posts eines Benutzers
def get_account_posts(db: Session, account_id: int):
    posts = db.query(Post, Account.username).join(Account).filter(Post.account_id == account_id).all()
    return [{
        "id": post.id,
        "account_id": post.account_id,
        "description": post.description,
        "base64_image": convert_image_to_base64(post.reduced_image),
        "username": username
    } for post, username in posts]


def get_post_full_image_by_id(db: Session, post_id: int):
    """
    Holt das full_image eines Posts anhand seiner ID.

    :param db: Session-Objekt für die Datenbankverbindung.
    :param post_id: Die ID des Posts.
    :return: Das full_image des Posts als Byte-Array oder None, falls der Post nicht gefunden wurde.
    """
    post = db.query(Post.full_image).filter(Post.id == post_id).first()
    if post and post.full_image:
        return convert_image_to_base64(post.full_image)
    else:
        return None



def get_post_comments(db: Session, post_id: int):
    comments_with_username = (
        db.query(Comment, Account.username)
        .join(Account, Comment.account_id == Account.id)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
        .all()
    )

    return [
        {
            "comment_id": comment.id,
            "account_id": comment.account_id,
            "text": comment.text,
            "created_at": comment.created_at,
            "username": username,
            "classifier": comment.classifier
        }
        for comment, username in comments_with_username
    ]

# Auslesen von 9 zufälligen Post die nicht dem User gehören (Für ein Feed)
def get_random_posts_not_by_account(db: Session, account_id: int):
    posts = db.query(Post, Account.username).join(Account, Post.account_id == Account.id).filter(Post.account_id != account_id).order_by(func.random()).limit(9).all()
    return [{
        "id": post.id,
        "account_id": post.account_id,
        "description": post.description,
        "base64_image": convert_image_to_base64(post.reduced_image),
        "username": username
    } for post, username  in posts]

# Löscht einen Post und alle dazugehörigen Kommentare
def delete_post(db: Session, post_id: int):
    # Suche den Post in der Datenbank über seine ID
    db_post = db.query(Post).filter(Post.id == post_id).first()

    # Überprüfe, ob der Post existiert
    if db_post is None:
        raise ValueError("Post mit der ID {} wurde nicht gefunden.".format(post_id))

    # Lösche zuerst alle Kommentare, die zu diesem Post gehören
    db.query(Comment).filter(Comment.post_id == post_id).delete()

    # Lösche den Post aus der Datenbank
    db.delete(db_post)
    db.commit()


# Löscht einen Account und alle damit verbundenen Profile, Posts und Kommentare
def delete_account(db: Session, account_id: int):
    with db.begin():
        # Suche den Account in der Datenbank über seine ID
        db_account = db.query(Account).filter(Account.id == account_id).first()

        if db_account is None:
            raise ValueError(f"Account mit der ID {account_id} wurde nicht gefunden.")

        # Lösche alle Kommentare, die vom Account erstellt wurden
        db.query(Comment).filter(Comment.account_id == account_id).delete(synchronize_session=False)

        # Lösche alle Kommentare von Posts des Accounts 
        db.query(Comment).filter(Comment.post_id.in_(
            db.query(Post.id).filter(Post.account_id == account_id)
        )).delete(synchronize_session=False)

        # Lösche alle Posts des Accounts
        db.query(Post).filter(Post.account_id == account_id).delete(synchronize_session=False)

        # Lösche das Profil, das zum Account gehört
        db.query(Profile).filter(Profile.account_id == account_id).delete(synchronize_session=False)

        # Lösche den Account
        db.delete(db_account)




