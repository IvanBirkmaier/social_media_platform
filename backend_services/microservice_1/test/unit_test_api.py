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

DATABASE_URL = "sqlite://"
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

def test_create_user_success():
    # Test a successful user creation
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = client.post("/account/", json=data)
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"

def test_create_user_duplicate_username():
    # Test creating a user with a duplicate username
    data = {
        "username": "testuser",  # Choose a username that already exists in your test database
        "email": "newuser@example.com",
        "password": "newpassword",
    }
    response = client.post("/account/", json=data)
    assert response.status_code == 400
    assert "Username already registered" in response.text
    
def test_create_profile_success():
    # Test a successful profile creation
    data = {
        "account_id": 1,
        "vorname": "John",
        "nachname": "Doe",
        "city": "Example City",
        "plz": 12345,
        "street": "Example Street",
        "phone_number": "123-456-7890",
    }
    response = client.post("/profile/", json=data)
    assert response.status_code == 201
    assert response.json()["vorname"] == "John"
    assert response.json()["nachname"] == "Doe"
    # Add more assertions for other fields in the response

def test_create_profile_invalid_data():
    # Test creating a profile with invalid data
    data = {
        # Missing required fields, or invalid data
    }
    response = client.post("/profile/", json=data)
    assert response.status_code == 422  # Assuming FastAPI returns a 422 for validation errors

from app import create_profile

def test_create_profile_duplicate_account_id():
    # Test creating a profile with a duplicate account_id
    # Ensure to create an initial profile with the same account_id for this test
    initial_data = {
        "account_id": 1,
        "vorname": "John",
        "nachname": "Doe",
        "city": "Example City",
        "plz": 12345,
        "street": "Example Street",
        "phone_number": "123-456-7890",
    }
    create_profile(TestingSessionLocal(), **initial_data)

    # Attempt to create a profile with the same account_id
    data = {
        "account_id": 1,
        "vorname": "Jane",
        "nachname": "Smith",
        "city": "New City",
        "plz": 54321,
        "street": "New Street",
        "phone_number": "987-654-3210",
    }
    response = client.post("/profile/", json=data)
    assert response.status_code == 400  # Assuming FastAPI returns a 400 for duplicate account_id

def test_check_username_exists():
    # Test when the username exists in the database
    existing_username = "existing_user"
    # Ensure to create an account with the existing username for this test
    create_account_with_username(TestingSessionLocal(), existing_username)

    response = client.get(f"/check_username/?username={existing_username}")
    assert response.status_code == 200
    assert response.json()["username_exists"] == True

def test_check_username_not_exists():
    # Test when the username does not exist in the database
    new_username = "new_user"

    response = client.get(f"/check_username/?username={new_username}")
    assert response.status_code == 200
    assert response.json()["username_exists"] == False

def create_account_with_username(db: Session, username: str):
    # Helper function to create an account with the given username
    # Use this function to set up the database state for testing
    # This function should be adapted based on your account creation logic
    data = {
        "username": str,
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = client.post("/account/", json=data)