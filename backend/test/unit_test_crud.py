import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from services.src.crud import hash_password, check_password_hash, create_account, create_profile, check_username_existence, check_email_existence, read_profile
from services.src.model import Account, Profile, Post, Comment

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

    # Mock the account creation process
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=None)  # mock_db.refresh doesn't need a specific return

    # Call create_account
    account = create_account(mock_db, "test_user", "test@example.com", "test_password")

    # Assertions
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()  # Modified to not expect a specific mock account
    assert isinstance(account, Account)  # Check if returned account is an instance of Account


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
    mock_db.refresh.assert_called_once()
    assert isinstance(profile, Profile)  # Check if returned account is an instance of Account
    
# def read_profile(db: Session, account_id: int):
def test_read_profile():
    mock_db = MagicMock()
    mock_profile = MagicMock()
    
    mock_profile.vorname = "Torben"
    mock_profile.nachname = "Testmann"
    mock_profile.city = "Teststadt"
    mock_profile.plz = "0815"
    mock_profile.street = "Testerstraße 1"
    mock_profile.phone_number = "0123456" 
    
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_profile)
    
    profile = create_profile(mock_db, 1, "Torben", "Testmann", "Teststadt", "0815", "Testerstraße 1", "0123456")
    
    mock_db.query().filter().first = MagicMock(return_value=mock_profile)
    db_profile = read_profile(mock_db, 1)
    
    assert db_profile.vorname == profile.vorname
    assert db_profile.nachname == profile.nachname
    assert db_profile.city == profile.city
    assert db_profile.plz == profile.plz
    assert db_profile.street == profile.street
    assert db_profile.phone_number == profile.phone_number
    
from services.src.crud import check_account_login

def test_check_account_login_valid_credentials():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating a sample account with hashed password
    username = "test_user"
    password = "test_password"
    hashed_password = hash_password(password)
    mock_account = Account(username=username, password_hash=hashed_password)

    # Mocking the database query result
    mock_db.query().filter().first = MagicMock(return_value=mock_account)

    # Calling the function with valid credentials
    result = check_account_login(mock_db, username, password)

    # Assertions
    assert result == mock_account
    
def test_check_account_login_invalid_credentials():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating a sample account with hashed password
    username = "test_user"
    password = "test_password"
    hashed_password = hash_password(password)
    mock_account = Account(username=username, password_hash=hashed_password)

    # Mocking the database query result (no account found)
    mock_db.query().filter().first = MagicMock(return_value=None)

    # Calling the function with invalid credentials
    result = check_account_login(mock_db, username, "wrong_password")

    # Assertions
    assert result is None
    
def test_check_account_login_no_account():
    # Mocking the database session
    mock_db = MagicMock()

    # Mocking the database query result (no account found)
    mock_db.query().filter().first = MagicMock(return_value=None)

    # Calling the function with non-existent username
    result = check_account_login(mock_db, "nonexistent_user", "password")

    # Assertions
    assert result is None
    
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
    mock_db.refresh.assert_called_once()
    assert isinstance(post, Post)
    

from services.src.crud import create_comment

# def create_post(db: Session, account_id: int, description: str, base64_image: str):
def test_create_comment():
    mock_db = MagicMock()
    mock_comment = MagicMock()
    
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_comment)
    
    comment = create_comment(mock_db, 1, 1, "Have a nice trip!")
    
    mock_db.query().filter().first = MagicMock(return_value=mock_comment)
    
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert isinstance(comment, Comment)
    
from services.src.crud import get_account_posts, convert_image_to_base64
from typing import List

def test_get_account_posts_with_posts():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating sample posts
    posts_data = [
        {"id": 1, "account_id": 1, "description": "Post 1", "image": b"image_data_1"},
        {"id": 2, "account_id": 1, "description": "Post 2", "image": b"image_data_2"},
    ]

    # Mocking the database query result
    mock_db.query().filter().all = MagicMock(return_value=[Post(**post_data) for post_data in posts_data])

    # Calling the function
    result = get_account_posts(mock_db, account_id=1)

    # Assertions
    assert len(result) == len(posts_data)
    for i, post_data in enumerate(posts_data):
        assert result[i]["id"] == post_data["id"]
        assert result[i]["account_id"] == post_data["account_id"]
        assert result[i]["description"] == post_data["description"]
        assert result[i]["base64_image"] == convert_image_to_base64(post_data["image"])
        
def test_get_account_posts_no_posts():
    # Mocking the database session
    mock_db = MagicMock()

    # Mocking the database query result (no posts found)
    mock_db.query().filter().all = MagicMock(return_value=[])

    # Calling the function with no posts
    result = get_account_posts(mock_db, account_id=1)

    # Assertions
    assert result == []

def test_get_account_posts_with_empty_image():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating a sample post with an empty image
    post_data = {"id": 1, "account_id": 1, "description": "Post 1", "image": None}
    # Mocking the database query result
    mock_db.query().filter().all = MagicMock(return_value=[Post(**post_data)])

    # Calling the function
    result = get_account_posts(mock_db, account_id=1)

    # Assertions
    assert len(result) == 1
    assert result[0]["id"] == post_data["id"]
    assert result[0]["account_id"] == post_data["account_id"]
    assert result[0]["description"] == post_data["description"]
    assert result[0]["base64_image"] is None
    
from services.src.crud import get_random_posts_not_by_account
    
def test_get_random_posts_not_by_account_with_posts():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating sample posts
    posts_data = [
        {"id": 1, "account_id": 2, "description": "Post 1", "image": b"image_data_1"},
        {"id": 2, "account_id": 3, "description": "Post 2", "image": b"image_data_2"},
    ]

    # Mocking the database query result
    mock_db.query().filter().order_by().limit().all = MagicMock(return_value=[Post(**post_data) for post_data in posts_data])

    # Calling the function
    result = get_random_posts_not_by_account(mock_db, account_id=1)

    # Assertions
    assert len(result) == len(posts_data)
    for i, post_data in enumerate(posts_data):
        assert result[i]["id"] == post_data["id"]
        assert result[i]["account_id"] == post_data["account_id"]
        assert result[i]["description"] == post_data["description"]
        assert result[i]["base64_image"] == convert_image_to_base64(post_data["image"])

def test_get_random_posts_not_by_account_no_posts():
    # Mocking the database session
    mock_db = MagicMock()

    # Mocking the database query result (no posts found)
    mock_db.query().filter().order_by().limit().all = MagicMock(return_value=[])

    # Calling the function with no posts
    result = get_random_posts_not_by_account(mock_db, account_id=1)

    # Assertions
    assert result == []

def test_get_random_posts_not_by_account_with_empty_image():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating a sample post with an empty image
    post_data = {"id": 1, "account_id": 2, "description": "Post 1", "image": None}

    # Mocking the database query result
    mock_db.query().filter().order_by().limit().all = MagicMock(return_value=[Post(**post_data)])

    # Calling the function
    result = get_random_posts_not_by_account(mock_db, account_id=1)

    # Assertions
    assert len(result) == 1
    assert result[0]["id"] == post_data["id"]
    assert result[0]["account_id"] == post_data["account_id"]
    assert result[0]["description"] == post_data["description"]
    assert result[0]["base64_image"] is None
    
from services.src.crud import delete_post

def test_delete_post_existing_post():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating a sample post
    post_data = {"id": 1, "account_id": 2, "description": "Post 1", "image": b"image_data_1"}
    existing_post = Post(**post_data)
    mock_db.query().filter().first = MagicMock(return_value=existing_post)

    # Calling the function with an existing post
    delete_post(mock_db, post_id=1)

    # Assertions
    mock_db.query().filter().first.assert_called_once_with()
    mock_db.delete.assert_called_once_with(existing_post)
    mock_db.commit.assert_called_once()

def test_delete_post_nonexistent_post():
    # Mocking the database session
    mock_db = MagicMock()

    # Mocking the database query result (no post found)
    mock_db.query().filter().first = MagicMock(return_value=None)

    # Calling the function with a nonexistent post
    with pytest.raises(ValueError, match="Post mit der ID 1 wurde nicht gefunden."):
        delete_post(mock_db, post_id=1)

    # Assertions
    mock_db.query().filter().first.assert_called_once_with()
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()