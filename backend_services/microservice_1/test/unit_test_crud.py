import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from microservice_1.src.crud import hash_password, check_password_hash, create_account, create_profile, check_username_existence, check_email_existence, read_profile
from microservice_1.src.model import Account, Profile, Post, Comment

import pytest
from unittest.mock import MagicMock

def test_create_account():
    # Mocking the database session
    mock_db = MagicMock()

    # Mocking the password hashing function
    mock_hash_password = MagicMock(return_value="hashed_password")
    
    # Creating a sample account data
    account_data = {"username": "test_user", "email": "test@example.com", "password": "test_password"}
    
    # Calling the create_account function
    with pytest.MonkeyPatch().context() as m:
        m.setattr("microservice_1.src.crud.hash_password", mock_hash_password)
        account = create_account(mock_db, **account_data)

    # Assertions
    mock_hash_password.assert_called_once_with("test_password")
    mock_db.add.assert_called_once_with(account)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(account)
    assert isinstance(account, Account)
    assert account.username == "test_user"
    assert account.email == "test@example.com"
    assert account.password_hash == "hashed_password"

def test_create_profile():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating a sample profile data
    profile_data = {
        "account_id": 1,
        "vorname": "John",
        "nachname": "Doe",
        "city": "New York",
        "plz": 10001,
        "street": "123 Main St",
        "phone_number": "555-1234"
    }

    # Calling the create_profile function
    profile = create_profile(mock_db, **profile_data)

    # Assertions
    mock_db.add.assert_called_once_with(profile) # Profile(account_id=1, vorname="John", nachname="Doe", city="New York", plz=10001, street="123 Main St", phone_number="555-1234"))
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(profile)
    assert isinstance(profile, Profile)
    assert profile.account_id == 1
    assert profile.vorname == "John"
    assert profile.nachname == "Doe"
    assert profile.city == "New York"
    assert profile.plz == 10001
    assert profile.street == "123 Main St"
    assert profile.phone_number == "555-1234"
    
def test_read_profile():
    # Mocking the database session
    mock_db = MagicMock()

    # Creating a sample profile data
    profile_data = {
        "account_id": 1,
        "vorname": "John",
        "nachname": "Doe",
        "city": "New York",
        "plz": 10001,
        "street": "123 Main St",
        "phone_number": "555-1234"
    }

    # Calling the create_profile function to add a profile to the database
    create_profile(mock_db, **profile_data)

    # Mocking the query result for reading the profile
    mock_db.query().filter().first = MagicMock(return_value=Profile(
        account_id=1,
        vorname="John",
        nachname="Doe",
        city="New York",
        plz=10001,
        street="123 Main St",
        phone_number="555-1234"
    ))

    # Calling the read_profile function
    profile = read_profile(mock_db, account_id=1)

    # Assertions
    mock_db.query().filter().first.assert_called_once_with()
    assert isinstance(profile, Profile)
    assert profile.account_id == 1
    assert profile.vorname == "John"
    assert profile.nachname == "Doe"
    assert profile.city == "New York"
    assert profile.plz == 10001
    assert profile.street == "123 Main St"
    assert profile.phone_number == "555-1234"

def test_check_username_existence():
    mock_db = MagicMock()
    mock_db.query().filter().first = MagicMock(return_value=None)
    
    assert not check_username_existence(mock_db, "test_user")

def test_check_email_existence():
    mock_db = MagicMock()
    mock_db.query().filter().first = MagicMock(return_value=True)
    
    assert check_email_existence(mock_db, "test@example.com")
    
from microservice_1.src.crud import check_account_login

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
    
# from microservice_1.src.crud import create_post

# def test_create_post():
#     # Mocking the database session
#     mock_db = MagicMock()

#     # Mocking the Kafka send function
#     mock_kafka_send_post_id = MagicMock()

#     # Creating a sample post data
#     post_data = {
#         "account_id": 1,
#         "description": "A beautiful sunset",
#         "base64_image": convert_image_to_base64(b"image_data_1")
#     }

#     # Calling the create_post function
#     with pytest.MonkeyPatch().context() as m:
#         m.setattr("microservice_1.src.crud.validate_image_bytes", lambda x: None)
#         #m.setattr("microservice_1.src.producer.kafka_send_post_id", mock_kafka_send_post_id)
#         post = create_post(mock_db, **post_data)
        
#     # Assertions
#     mock_db.add.assert_called_once_with(post)
#     mock_db.commit.assert_called_once()
#     mock_db.refresh.assert_called_once_with(post)
#     #mock_kafka_send_post_id.assert_called_once_with(post["post_id"])  # Adjusted for the modified function
#     assert isinstance(post, dict)
#     assert post["post_id"] == 1  # Adjusted based on the mocked data
#     assert post["description"] == "A beautiful sunset"
    
# from microservice_1.src.crud import create_comment    

# def test_create_comment():
#     # Mocking the database session
#     mock_db = MagicMock()

#     # Mocking the Kafka send function
#     mock_kafka_send_comment_id = MagicMock()

#     # Creating a sample comment data
#     comment_data = {
#         "account_id": 1,
#         "post_id": 1,
#         "text": "Great post!"
#     }

#     # Calling the create_comment function
#     with pytest.MonkeyPatch().context() as m:
#         m.setattr("microservice_1.src.producer.kafka_send_comment_id", mock_kafka_send_comment_id)
#         comment = create_comment(mock_db, **comment_data)

#     # Assertions
#     mock_db.add.assert_called_once_with(comment)
#     mock_db.commit.assert_called_once()
#     mock_db.refresh.assert_called_once_with(comment)
# #    mock_kafka_send_comment_id.assert_called_once_with(comment.id)
#     assert isinstance(comment, Comment)
#     assert comment.account_id == 1
#     assert comment.post_id == 1
#     assert comment.text == "Great post!"

from microservice_1.src.crud import get_account_id_by_username
    
def test_get_account_id_by_username_exists():
    # Arrange
    mock_db = MagicMock()
    mock_account = MagicMock(id=1, username="username")
    
    # Mock the query method to return the mock_account
    mock_db.query(Account).filter(Account.username == "username").first.return_value = mock_account

    # Act
    account_id = get_account_id_by_username(mock_db, "username")

    # Assert
    assert account_id == 1
    mock_db.query(Account).filter(Account.username == "username").first.assert_called_once()

def test_get_account_id_by_username_not_exists():
    # Arrange
    mock_db = MagicMock()

    # Mock the query method to return None (account not found)
    mock_db.query(Account).filter(Account.username == "no_name").first.return_value = None

    # Act
    account_id = get_account_id_by_username(mock_db, "no_name")

    # Assert
    assert account_id is None
    mock_db.query(Account).filter(Account.username == "no_name").first.assert_called_once()
    

from microservice_1.src.crud import get_account_posts, convert_image_to_base64
from typing import List

def test_get_account_posts_with_posts():
    # Arrange
    mock_db = MagicMock()
    mock_post = MagicMock()
    mock_post.reduced_image = None
    mock_account = MagicMock()
    
    # Set up a mock query result with a post
    mock_db.query(Post, Account.username).join(Account).filter(Post.account_id == 1).all.return_value = [(mock_post, "user1")]
    
    # Act
    result = get_account_posts(mock_db, account_id=1)

    # Assert
    assert len(result) == 1
    assert result[0]["id"] == mock_post.id
    assert result[0]["account_id"] == mock_post.account_id
    assert result[0]["description"] == mock_post.description
    assert result[0]["base64_image"] == None
    assert result[0]["username"] == "user1"
    mock_db.query().join().filter().all.assert_called_once_with()

def test_get_account_posts_without_posts():
    # Arrange
    mock_db = MagicMock()
    
    # Set up a mock query result without posts
    mock_db.query(Post, Account.username).join(Account).filter(Post.account_id == 2).all.return_value = []
    
    # Act
    result = get_account_posts(mock_db, account_id=2)

    # Assert
    assert result == []
    mock_db.query().join().filter().all.assert_called_once_with()
    
from microservice_1.src.crud import get_post_full_image_by_id

def test_get_post_full_image_by_id_with_full_image():
    # Arrange
    mock_db = MagicMock()
    mock_post = MagicMock()
    mock_post.id = 1
    mock_post.full_image = None
    
    # Set up a mock query result with a post
    mock_db.query(Post.full_image).filter(Post.id == 1).first.return_value = mock_post
    
    # Act
    result = get_post_full_image_by_id(mock_db, post_id=1)

    # Assert
    assert result == None
    mock_db.query().filter().first.assert_called_once_with()

def test_get_post_full_image_by_id_without_full_image():
    # Arrange
    mock_db = MagicMock()
    mock_post = MagicMock()
    mock_post.id = 2
    mock_post.full_image = None
    
    # Set up a mock query result without full image
    mock_db.query(Post.full_image).filter(Post.id == 2).first.return_value = mock_post
    
    # Act
    result = get_post_full_image_by_id(mock_db, post_id=2)

    # Assert
    assert result is None
    mock_db.query().filter().first.assert_called_once_with()

from unittest.mock import patch
from microservice_1.src.crud import get_post_comments

@patch("microservice_1.src.crud.db")
def test_get_post_comments_with_comments(mock_db):
    # Arrange
    mock_comment1 = MagicMock()
    mock_comment2 = MagicMock()
    
    mock_comment1.id = 1
    mock_comment1.account_id = 1
    mock_comment1.text = "Mock Comment 1"
    mock_comment1.created_at = "2022-01-01 12:00:00"
    mock_comment1.classifier = "positive"
    
    mock_comment2.id = 2
    mock_comment2.account_id = 2
    mock_comment2.text = "Mock Comment 2"
    mock_comment2.created_at = "2022-01-02 12:00:00"
    mock_comment2.classifier = "negative"
    
    # Set up a mock query result with comments
    mock_comments_with_username = [
        (mock_comment1, "user1"),
        (mock_comment2, "user2")
    ]
    mock_db.query().join().filter().order_by().all.return_value = mock_comments_with_username
    
    # Act
    result = get_post_comments(mock_db, post_id=1)

    # Assert
    expected_result = [
        {
            "comment_id": mock_comment1.id,
            "account_id": mock_comment1.account_id,
            "text": mock_comment1.text,
            "created_at": mock_comment1.created_at,
            "username": "user1",
            "classifier": mock_comment1.classifier
        },
        {
            "comment_id": mock_comment2.id,
            "account_id": mock_comment2.account_id,
            "text": mock_comment2.text,
            "created_at": mock_comment2.created_at,
            "username": "user2",
            "classifier": mock_comment2.classifier
        }
    ]
    assert result == expected_result
    mock_db.query().join().filter().order_by().all.assert_called_once_with()

@patch("microservice_1.src.crud.db")
def test_get_post_comments_without_comments(mock_db):
    # Arrange
    
    # Set up a mock query result without comments
    mock_db.query().join().filter().order_by().all.return_value = []
    
    # Act
    result = get_post_comments(mock_db, post_id=2)

    # Assert
    assert result == []
    mock_db.query().join().filter().order_by().all.assert_called_once_with()

from microservice_1.src.crud import get_random_posts_not_by_account
    
@patch("microservice_1.src.crud.db")
def test_get_random_posts_not_by_account(mock_db):
    # Arrange
    mock_post1 = MagicMock()
    mock_post2 = MagicMock()
    
    mock_post1.id = 1
    mock_post1.account_id = 2
    mock_post1.description = "Mock Post 1"
    mock_post1.reduced_image = b"mock_image_data_1"
    
    mock_post2.id = 2
    mock_post2.account_id = 3
    mock_post2.description = "Mock Post 2"
    mock_post2.reduced_image = b"mock_image_data_2"
    
    # Set up a mock query result with posts
    mock_posts_with_username = [
        (mock_post1, "user2"),
        (mock_post2, "user3")
    ]
    mock_db.query().join().filter().order_by().limit().all.return_value = mock_posts_with_username
    
    # Act
    result = get_random_posts_not_by_account(mock_db, account_id=1)

    # Assert
    expected_result = [
        {
            "id": mock_post1.id,
            "account_id": mock_post1.account_id,
            "description": mock_post1.description,
            "base64_image": "mock_base64_image_data_1",
            "username": "user2"
        },
        {
            "id": mock_post2.id,
            "account_id": mock_post2.account_id,
            "description": mock_post2.description,
            "base64_image": "mock_base64_image_data_2",
            "username": "user3"
        }
    ]
    assert result == expected_result
    mock_db.query().join().filter().order_by().limit().all.assert_called_once_with()
