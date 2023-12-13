import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from services.src.crud import hash_password, check_password_hash, create_account, create_profile, check_username_existence, check_email_existence, read_profile

import pytest
from unittest.mock import MagicMock

def test_hash_and_check_password():
    password = "test_password"
    hashed_password = hash_password(password)

    # Überprüfen, ob das gehashte Passwort nicht gleich dem ursprünglichen Passwort ist
    assert hashed_password != password

    # Überprüfen, ob das Passwort korrekt verifiziert wird
    assert check_password_hash(password, hashed_password)

def test_create_account():
    mock_db = MagicMock()
    mock_account = MagicMock()

    # Annahme, dass der Account erstellt wurde
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_account)

    account = create_account(mock_db, "test_user", "test@example.com", "test_password")

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_account)
    assert account == mock_account

def test_check_username_existence():
    mock_db = MagicMock()
    mock_db.query().filter().first = MagicMock(return_value=None)
    
    assert not check_username_existence(mock_db, "test_user")

def test_check_email_existence():
    mock_db = MagicMock()
    mock_db.query().filter().first = MagicMock(return_value=True)
    
    assert check_email_existence(mock_db, "test@example.com")

# def create_profile(db: Session, account_id: int, vorname: str, nachname: str, city: str, plz: int, street: str, phone_number: str):    
def test_create_profile():
    mock_db = MagicMock()
    mock_profile = MagicMock()

    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_profile)
    
    profile = create_profile(mock_db, 1, "Torben", "Testmann", "Teststadt", "0815", "Testerstraße 1", "0123456")
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_profile)
    assert profile == mock_profile
    
# def read_profile(db: Session, account_id: int):
def test_read_profile():
    mock_db = MagicMock()
    mock_profile = MagicMock()
    
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_profile)
    
    profile = create_profile(mock_db, 1, "Torben", "Testmann", "Teststadt", "0815", "Testerstraße 1", "0123456")
    
    mock_db.query().filter().first = MagicMock(return_value=None)
    db_profile = read_profile(mock_db, 1)
    assert db_profile.vorname == profile.vorname
    assert db_profile.nachname == profile.nachname
    assert db_profile.city == profile.city
    assert db_profile.plz == profile.plz
    assert db_profile.street == profile.street
    assert db_profile.phone_number == profile.phone_number
    
from services.src.crud import check_account_login

# def check_account_login(db: Session, username: str, password: str):
def test_check_account_login():
    mock_db = MagicMock()
    mock_account = MagicMock()

    # Annahme, dass der Account erstellt wurde
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_account)

    account = create_account(mock_db, "test_user", "test@example.com", "test_password")
    
    mock_db.query().filter().first = MagicMock(return_value=None)
    db_account = check_account_login(mock_db, "test_user", "test_password")
    assert db_account == account
    assert db_account != None

def test_check_account_login_failed():
    mock_db = MagicMock()
    mock_account = MagicMock()

    # Annahme, dass der Account erstellt wurde
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_account)

    account = create_account(mock_db, "test_user", "test@example.com", "test_password")
    
    mock_db.query().filter().first = MagicMock(return_value=None)
    db_account = check_account_login(mock_db, "test_user", "password")
    assert db_account == None
    
from services.src.crud import create_post

# def create_post(db: Session, account_id: int, description: str, base64_image: str):
def test_create_post():
    mock_db = MagicMock()
    mock_post = MagicMock()
    
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_post)
    
    post = create_post(mock_db, 1, "Greetings from Vienna", "")
    
    mock_db.query().filter().first = MagicMock(return_value=None)
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_post)
    assert post == mock_post
    

from services.src.crud import create_comment

# def create_post(db: Session, account_id: int, description: str, base64_image: str):
def test_create_post():
    mock_db = MagicMock()
    mock_comment = MagicMock()
    
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_comment)
    
    comment = create_comment(mock_db, 1, 1, "Have a nice trip!")
    
    mock_db.query().filter().first = MagicMock(return_value=None)
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_comment)
    assert comment == mock_comment
    
    