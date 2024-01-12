from sqlalchemy.orm import Session
from .model import Account, Profile, Post, Comment
import bcrypt
import logging


logging.basicConfig(level=logging.INFO)



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

# Funktion, um die Account-ID anhand des Benutzernamens zu finden
def get_account_id_by_username(db: Session, username: str):
    account = db.query(Account).filter(Account.username == username).first()
    if account:
        return account.id
    else:
        return None

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




