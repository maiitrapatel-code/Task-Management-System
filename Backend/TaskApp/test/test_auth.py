"""
test_auth.py - Authentication Tests

Tests for user signup, login, and logout endpoints.
These verify that authentication works correctly.

HOW TO RUN:
    pytest test/test_auth.py -v

WHAT -v DOES:
    Shows verbose output with each test name and result
"""

import pytest
from fastapi import status


# =============================================================================
# SIGNUP TESTS
# =============================================================================

class TestSignup:
    """Tests for POST /auth/signup endpoint"""
    
    def test_signup_success(self, client):
        """
        Test: Creating a new user should succeed.
        
        Expected: 201 Created with success message
        """
        response = client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "User created successfully"
    
    
    def test_signup_duplicate_email(self, client, test_user):
        """
        Test: Signing up with an existing email should fail.
        
        Expected: 400 Bad Request with error message
        """
        response = client.post(
            "/auth/signup",
            json={
                "username": "differentuser",
                "email": test_user["email"],  # Same email as existing user
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    
    def test_signup_duplicate_username(self, client, test_user):
        """
        Test: Signing up with an existing username should fail.
        
        Expected: 400 Bad Request with error message
        """
        response = client.post(
            "/auth/signup",
            json={
                "username": test_user["username"],  # Same username
                "email": "different@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]
    
    
    def test_signup_invalid_email(self, client):
        """
        Test: Signing up with invalid email format should fail.
        
        Expected: 422 Unprocessable Entity (validation error)
        """
        response = client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "not-an-email",  # Invalid email format
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_signup_short_password(self, client):
        """
        Test: Signing up with too short password should fail.
        
        Expected: 422 Unprocessable Entity (validation error)
        """
        response = client.post(
            "/auth/signup",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "123"  # Too short (less than 6 chars)
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_signup_short_username(self, client):
        """
        Test: Signing up with too short username should fail.
        
        Expected: 422 Unprocessable Entity (validation error)
        """
        response = client.post(
            "/auth/signup",
            json={
                "username": "ab",  # Too short (less than 3 chars)
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# =============================================================================
# LOGIN TESTS
# =============================================================================

class TestLogin:
    """Tests for POST /auth/login endpoint"""
    
    def test_login_success(self, client, test_user):
        """
        Test: Logging in with correct credentials should succeed.
        
        Expected: 200 OK with access_token
        """
        response = client.post(
            "/auth/login",
            data={  # Note: login uses form data, not JSON
                "username": test_user["username"],
                "password": test_user["password"]
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    
    def test_login_wrong_password(self, client, test_user):
        """
        Test: Logging in with wrong password should fail.
        
        Expected: 401 Unauthorized
        """
        response = client.post(
            "/auth/login",
            data={
                "username": test_user["username"],
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_login_nonexistent_user(self, client):
        """
        Test: Logging in with non-existent user should fail.
        
        Expected: 401 Unauthorized
        """
        response = client.post(
            "/auth/login",
            data={
                "username": "nonexistent",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# LOGOUT TESTS
# =============================================================================

class TestLogout:
    """Tests for POST /auth/logout endpoint"""
    
    def test_logout_success(self, client, auth_headers):
        """
        Test: Logging out with valid token should succeed.
        
        Expected: 200 OK with success message
        """
        response = client.post("/auth/logout", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Successfully logged out"
    
    
    def test_logout_without_token(self, client):
        """
        Test: Logging out without token should fail.
        
        Expected: 401 Unauthorized
        """
        response = client.post("/auth/logout")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
