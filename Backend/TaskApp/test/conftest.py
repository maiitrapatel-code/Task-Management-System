"""
conftest.py - Test Configuration & Fixtures

This file contains shared test fixtures that are automatically 
available to all test files. Pytest discovers this file automatically.

KEY CONCEPTS:
- Fixtures: Reusable setup code that provides data/objects to tests
- Test Database: We use a separate SQLite database for testing (not PostgreSQL)
- Dependency Override: We replace the real database with test database
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import our app and database components
from main import app
from database import Base, get_db
from routers.auth import bcrypt_context

# =============================================================================
# TEST DATABASE SETUP
# =============================================================================
# We use SQLite in-memory database for tests (fast & isolated)
# This means each test run starts with a fresh, empty database

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    poolclass=StaticPool,  # Use same connection for all threads
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture(scope="function")
def test_db():
    """
    Creates a fresh database for each test function.
    
    - Before test: Creates all tables
    - After test: Drops all tables (cleanup)
    
    This ensures tests are isolated and don't affect each other.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Creates a test client that uses the test database.
    
    The TestClient lets us make HTTP requests to our FastAPI app
    without running a real server.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    # Replace the real database dependency with test database
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    yield TestClient(app)
    
    # Cleanup: Remove the override
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    """
    Creates a test user and returns their credentials.
    
    This fixture is useful when you need an existing user
    to test login or other user-dependent features.
    """
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    # Create the user via API
    client.post("/auth/signup", json=user_data)
    
    return user_data


@pytest.fixture
def auth_headers(client, test_user):
    """
    Creates a test user, logs them in, and returns authorization headers.
    
    Use this when testing protected endpoints that require JWT token.
    
    Returns:
        dict: Headers with Bearer token, e.g., {"Authorization": "Bearer <token>"}
    """
    # Login to get token
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_task(client, auth_headers):
    """
    Creates a test task and returns its data.
    
    Use this when you need an existing task to test update/delete.
    """
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": 3,
        "complete": False
    }
    
    response = client.post("/tasks/", json=task_data, headers=auth_headers)
    
    # Get the created task (fetch all and get the first one)
    tasks_response = client.get("/tasks/", headers=auth_headers)
    created_task = tasks_response.json()[0]
    
    return {**task_data, "id": created_task["id"]}
