from sqlalchemy.orm import Session
from sqlalchemy import func
from .model import Account, Post, Comment
from .producer import kafka_send_post_id
import base64
from PIL import Image
import io
from mimetypes import guess_type
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO)


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
    logging.info(f"##KAFKA: POST ID {db_post.id} erfolgreich an Server gesendet...")
    return db_post.id

def convert_image_to_base64(image_bytes):
    if image_bytes:
        image_stream = BytesIO(image_bytes)
        image_format = Image.open(image_stream).format.lower()
        mime_type, _ = guess_type(f".{image_format}")
        base64_encoded = base64.b64encode(image_bytes).decode('utf-8')
        return f"data:{mime_type};base64,{base64_encoded}"
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

# Vollsized image
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
