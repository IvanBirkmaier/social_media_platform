import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest 
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.declarative import declarative_base
    
from microservice_1.src.model import Base
from app import app, get_db

DATABASE_URL = "sqlite:///:memory:"
#engine = create_engine(DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test case for creating a new user successfully
def test_create_user_endpoint_success():
    # Arrange
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }

    # Act
    response = client.post("/account/", json=user_data)

    # Assert
    assert response.status_code == 201
    assert response.json() == {"id" : 1, "username": "testuser", "email": "test@example.com"}

# Test case for creating a user with a duplicate username
def test_create_user_endpoint_duplicate_username():
    # Arrange
    user_data = {
        "username": "newuser",  # Assuming this username already exists in the test database
        "email": "newuser@example.com",
        "password": "newuserpassword",
    }

    # Act
    response = client.post("/account/", json=user_data)
    response = client.post("/account/", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

from unittest.mock import patch

# Test case for getting account ID by username (account exists)
def test_get_account_id_username_exists():
    # Arrange
    username = "testuser"  # Replace with an existing username in your test database

    # Mock the get_account_id_by_username function to return a known account ID
    with patch("microservice_1.src.crud.get_account_id_by_username") as mock_get_account_id:
        mock_get_account_id.return_value = 1

        # Act
        response = client.get(f"/account-id/{username}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"account_id": 1}

# Test case for getting account ID by username (account does not exist)
def test_get_account_id_username_not_exists():
    # Arrange
    username = "nonexistentuser"  # Replace with a non-existing username in your test database

    # Mock the get_account_id_by_username function to return None (account not found)
    with patch("microservice_1.src.crud.get_account_id_by_username") as mock_get_account_id:
        mock_get_account_id.return_value = None

        # Act
        response = client.get(f"/account-id/{username}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"account_id": 0}

from fastapi import status

def test_create_profile_endpoint():
    # Arrange
    profile_data = {
        "account_id": 1,
        "vorname": "John",
        "nachname": "Doe",
        "city": "New York",
        "plz": 10001,
        "street": "123 Main St",
        "phone_number": "123-456-7890"
    }

    # Mock the create_profile function to return a known profile
    with patch("microservice_1.src.crud.create_profile") as mock_create_profile:
        mock_create_profile.return_value = {**profile_data}

        # Act
        response = client.post("/profile/", json=profile_data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    
    assert response.json() == {**profile_data}
    #assert response.json() == {"profile_id": 1, **profile_data}

def test_check_username_endpoint_username_exists():
    # Arrange
    username = "testuser"

    # Mock the check_username_existence function to return True
    with patch("microservice_1.src.crud.check_username_existence") as mock_check_username_existence:
        mock_check_username_existence.return_value = True

        # Act
        response = client.get(f"/check-username/{username}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"username_exists": True}

def test_check_username_endpoint_username_does_not_exist():
    # Arrange
    username = "nonexistent_user"

    # Mock the check_username_existence function to return False
    with patch("microservice_1.src.crud.check_username_existence") as mock_check_username_existence:
        mock_check_username_existence.return_value = False

        # Act
        response = client.get(f"/check-username/{username}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"username_exists": False}

def test_check_email_endpoint_email_exists():
    # Arrange
    email = "newuser@example.com"

    # Mock the check_email_existence function to return True
    with patch("microservice_1.src.crud.check_email_existence") as mock_check_email_existence:
        mock_check_email_existence.return_value = True

        # Act
        response = client.get(f"/check-email/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"email_exists": True}

def test_check_email_endpoint_email_does_not_exist():
    # Arrange
    email = "nonexistent_email@example.com"

    # Mock the check_email_existence function to return False
    with patch("microservice_1.src.crud.check_email_existence") as mock_check_email_existence:
        mock_check_email_existence.return_value = False

        # Act
        response = client.get(f"/check-email/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"email_exists": False}

from app import UserLogin
from microservice_1.src.crud import create_account

def test_login_successful():
    # Arrange
    username = "test_user"
    password = "test_password"
    user_login = UserLogin(username=username, password=password)

    # Create a user in the test database
    with override_get_db() as mock_db:
        create_account(mock_db, username, "test@example.com", password)

    # Act
    response = client.post("/login/", json=user_login.dict())

    # Assert
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": username}

def test_login_failed():
    # Arrange
    username = "test_user"
    password = "test_password"
    user_login = UserLogin(username=username, password="wrong_password")

    # Act
    response = client.post("/login/", json=user_login.dict())

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Falscher Benutzername oder Passwort"}
    
from unittest.mock import MagicMock

def test_create_post_successful():
    # Arrange
    with patch("microservice_1.src.crud.create_post", side_effect=ValueError("Test DB Error")):
        post_data = {
            "account_id": 1,
            "description": "Test Post",
            "base64_image": None
        }

    # Act
    response = client.post("/posts/", json=post_data)

    # Assert
    assert response.status_code == 201
    assert "post_id" in response.json()


def test_create_post_db_error():
    # Arrange
    with patch("microservice_1.src.crud.create_post", side_effect=ValueError("Test DB Error")):
        post_data = {
            "account_id": 1,
            "description": "Test Post",
            "base64_image": None
        }

        # Act
        response = client.post("/posts/", json=post_data)

        # Assert
        assert response.status_code == 500
        assert "detail" in response.json()
        
# def test_create_comment_successful():
#     # Arrange
#     mock_db = MagicMock()
#     mock_db.add.return_value = None  # Adjust based on the behavior of your create_comment function
    
#     comment_data = {
#         "account_id": 1,
#         "post_id": 2,
#         "text": "Test Comment"
#     }

#     # Act
#     response = client.post("/comments/", json=comment_data)

#     # Assert
#     assert response.status_code == 201
#     assert "comment_id" in response.json()

# def test_create_comment_db_error():
#     # Arrange
#     with patch("microservice_1.src.crud.create_comment", side_effect=ValueError("Test DB Error")):
#         comment_data = {
#             "account_id": 1,
#             "post_id": 2,
#             "text": "Test Comment"
#         }

#         # Act
#         response = client.post("/comments/", json=comment_data)

#         # Assert
#         assert response.status_code == 500
#         assert "detail" in response.json()

def test_get_posts_by_user_successful():
    # Arrange
    mock_db = MagicMock()
    mock_posts = [
        {"id": 1, "account_id": 1, "description": "Test Post 1", "base64_image": "mock_base64_image_1"},
        {"id": 2, "account_id": 1, "description": "Test Post 2", "base64_image": "mock_base64_image_2"}
    ]
    with patch("microservice_1.src.crud.get_account_posts", return_value=mock_posts):
        # Act
        response = client.get("/account/1/posts/")

        # Assert
        assert response.status_code == 200
        assert "posts" in response.json()
        assert len(response.json()["posts"]) == len(mock_posts)

def test_get_posts_by_user_no_posts():
    # Arrange
    mock_db = MagicMock()
    with patch("microservice_1.src.crud.get_account_posts", return_value=[]):
        # Act
        response = client.get("/account/1/posts/")

        # Assert
        assert response.status_code == 200
        assert "posts" in response.json()
        assert len(response.json()["posts"]) == 0
        
def test_get_comments_by_post_successful():
    # Arrange
    mock_db = MagicMock()
    mock_comments = [
        {"comment_id": 1, "account_id": 1, "text": "Test Comment 1"},
        {"comment_id": 2, "account_id": 1, "text": "Test Comment 2"}
    ]
    with patch("microservice_1.src.crud.get_post_comments", return_value=mock_comments):
        # Act
        response = client.get("/posts/1/comments/")

        # Assert
        assert response.status_code == 200
        assert "comments" in response.json()
        assert len(response.json()["comments"]) == len(mock_comments)

def test_get_comments_by_post_no_comments():
    # Arrange
    mock_db = MagicMock()
    with patch("microservice_1.src.crud.get_post_comments", return_value=None):
        # Act
        response = client.get("/posts/1/comments/")

        # Assert
        assert response.status_code == 200
        assert "comments" in response.json()
        assert len(response.json()["comments"]) == 0
        
def test_get_random_posts_successful():
    # Arrange
    mock_db = MagicMock()
    mock_posts = [
        {"id": 1, "account_id": 2, "description": "Test Post 1"},
        {"id": 2, "account_id": 3, "description": "Test Post 2"}
    ]
    with patch("microservice_1.src.crud.get_random_posts_not_by_account", return_value=mock_posts):
        # Act
        response = client.get("/posts/random/?account_id=1")

        # Assert
        assert response.status_code == 200
        assert "posts" in response.json()
        assert len(response.json()["posts"]) == len(mock_posts)

def test_get_random_posts_no_posts():
    # Arrange
    mock_db = MagicMock()
    with patch("microservice_1.src.crud.get_random_posts_not_by_account", return_value=[]):  # Change to return an empty list for no posts
        # Act
        response = client.get("/posts/random/?account_id=1")

        # Assert
        assert response.status_code == 200
        assert "posts" in response.json()
        assert len(response.json()["posts"]) == 0
        
def test_delete_account_successful():
    # Arrange
    mock_db = MagicMock()
    account_id = 1

    with patch("microservice_1.src.crud.delete_account"):
        # Act
        response = client.delete(f"/account/{account_id}/")

        # Assert
        assert response.status_code == 204
        assert response.text == "{\"detail\":\"Account successfully deleted\"}"

def test_delete_account_not_found():
    # Arrange
    mock_db = MagicMock()
    account_id = 1
    error_message = "Account mit der ID 1 wurde nicht gefunden."

    with patch("microservice_1.src.crud.delete_account", side_effect=ValueError(error_message)):
        # Act
        response = client.delete(f"/account/{account_id}/")

        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": error_message}
        
def test_delete_post_successful():
    # Arrange
    mock_db = MagicMock()
    post_id = 1

    with patch("microservice_1.src.crud.delete_post"):
        # Act
        response = client.delete(f"/posts/{post_id}/")

        # Assert
        assert response.status_code == 204
        assert response.text == ""

def test_delete_post_not_found():
    # Arrange
    mock_db = MagicMock()
    post_id = 1
    error_message = "Post mit der ID 1 wurde nicht gefunden."

    with patch("microservice_1.src.crud.delete_post", side_effect=ValueError(error_message)):
        # Act
        response = client.delete(f"/posts/{post_id}/")

        # Assert
        assert response.status_code == 404
        assert response.json() == {"detail": error_message}