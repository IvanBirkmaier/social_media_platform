import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import pytest 
from fastapi.testclient import TestClient
from app import app, create_tables, get_db, engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.src.model import Account, SessionLocal, Base, engine

# Use pytest-postgresql to manage a test PostgreSQL database
pytest_plugins = ["pytest_postgresql"]

# Override the dependency to use the testing database
app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

# Create tables in the testing database
create_tables()

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