"""
test_tasks.py - Task API Tests

Tests for CRUD operations on tasks (Create, Read, Update, Delete).
All task endpoints are protected and require JWT authentication.

HOW TO RUN:
    pytest test/test_tasks.py -v
"""

import pytest
from fastapi import status


# =============================================================================
# CREATE TASK TESTS
# =============================================================================

class TestCreateTask:
    """Tests for POST /tasks/ endpoint"""
    
    def test_create_task_success(self, client, auth_headers):
        """
        Test: Creating a task with valid data should succeed.
        
        Expected: 201 Created
        """
        task_data = {
            "title": "My New Task",
            "description": "Task description here",
            "priority": 3,
            "complete": False
        }
        
        response = client.post("/tasks/", json=task_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_201_CREATED
    
    
    def test_create_task_without_auth(self, client):
        """
        Test: Creating a task without token should fail.
        
        Expected: 401 Unauthorized
        """
        task_data = {
            "title": "My Task",
            "description": "Description",
            "priority": 3,
            "complete": False
        }
        
        response = client.post("/tasks/", json=task_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_create_task_invalid_priority(self, client, auth_headers):
        """
        Test: Creating a task with invalid priority should fail.
        
        Priority must be between 1-5 (gt=0, lt=6)
        Expected: 422 Unprocessable Entity
        """
        task_data = {
            "title": "My Task",
            "description": "Description",
            "priority": 10,  # Invalid: > 5
            "complete": False
        }
        
        response = client.post("/tasks/", json=task_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    def test_create_task_short_title(self, client, auth_headers):
        """
        Test: Creating a task with too short title should fail.
        
        Expected: 422 Unprocessable Entity
        """
        task_data = {
            "title": "AB",  # Too short (< 3 chars)
            "description": "Description",
            "priority": 3,
            "complete": False
        }
        
        response = client.post("/tasks/", json=task_data, headers=auth_headers)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# =============================================================================
# READ TASKS TESTS
# =============================================================================

class TestReadTasks:
    """Tests for GET /tasks/ endpoint"""
    
    def test_read_tasks_empty(self, client, auth_headers):
        """
        Test: Reading tasks when none exist should return empty list.
        
        Expected: 200 OK with empty array
        """
        response = client.get("/tasks/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    
    def test_read_tasks_with_data(self, client, auth_headers, test_task):
        """
        Test: Reading tasks should return user's tasks.
        
        Expected: 200 OK with array containing the task
        """
        response = client.get("/tasks/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == test_task["title"]
    
    
    def test_read_tasks_without_auth(self, client):
        """
        Test: Reading tasks without token should fail.
        
        Expected: 401 Unauthorized
        """
        response = client.get("/tasks/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_user_can_only_see_own_tasks(self, client, auth_headers, test_task):
        """
        Test: Users should only see their own tasks, not others'.
        
        Steps:
        1. User 1 creates a task (via test_task fixture)
        2. Create User 2 and login
        3. User 2 should see empty task list
        """
        # Create second user
        client.post(
            "/auth/signup",
            json={
                "username": "user2",
                "email": "user2@example.com",
                "password": "password123"
            }
        )
        
        # Login as second user
        login_response = client.post(
            "/auth/login",
            data={"username": "user2", "password": "password123"}
        )
        user2_token = login_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # User 2 should see no tasks (User 1's task is hidden)
        response = client.get("/tasks/", headers=user2_headers)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []  # Empty - can't see User 1's tasks


# =============================================================================
# UPDATE TASK TESTS
# =============================================================================

class TestUpdateTask:
    """Tests for PUT /tasks/{task_id} endpoint"""
    
    def test_update_task_success(self, client, auth_headers, test_task):
        """
        Test: Updating a task should succeed.
        
        Expected: 204 No Content
        """
        updated_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "priority": 5,
            "complete": True
        }
        
        response = client.put(
            f"/tasks/{test_task['id']}", 
            json=updated_data, 
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify the update
        get_response = client.get("/tasks/", headers=auth_headers)
        tasks = get_response.json()
        assert tasks[0]["title"] == "Updated Title"
        assert tasks[0]["complete"] == True
    
    
    def test_update_task_not_found(self, client, auth_headers):
        """
        Test: Updating a non-existent task should fail.
        
        Expected: 404 Not Found
        """
        updated_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "priority": 5,
            "complete": True
        }
        
        response = client.put(
            "/tasks/99999",  # Non-existent ID
            json=updated_data, 
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_update_task_without_auth(self, client, test_task):
        """
        Test: Updating a task without token should fail.
        
        Expected: 401 Unauthorized
        """
        updated_data = {
            "title": "Updated",
            "description": "Updated",
            "priority": 5,
            "complete": True
        }
        
        # Note: test_task needs auth_headers, so we use ID 1
        response = client.put("/tasks/1", json=updated_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# DELETE TASK TESTS
# =============================================================================

class TestDeleteTask:
    """Tests for DELETE /tasks/{task_id} endpoint"""
    
    def test_delete_task_success(self, client, auth_headers, test_task):
        """
        Test: Deleting an existing task should succeed.
        
        Expected: 204 No Content
        """
        response = client.delete(
            f"/tasks/{test_task['id']}", 
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify deletion
        get_response = client.get("/tasks/", headers=auth_headers)
        assert get_response.json() == []
    
    
    def test_delete_task_not_found(self, client, auth_headers):
        """
        Test: Deleting a non-existent task should fail.
        
        Expected: 404 Not Found
        """
        response = client.delete("/tasks/99999", headers=auth_headers)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    
    def test_delete_task_without_auth(self, client):
        """
        Test: Deleting a task without token should fail.
        
        Expected: 401 Unauthorized
        """
        response = client.delete("/tasks/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    def test_cannot_delete_other_users_task(self, client, auth_headers, test_task):
        """
        Test: Users should not be able to delete other users' tasks.
        
        Steps:
        1. User 1 creates a task (via test_task fixture)
        2. Create User 2 and try to delete User 1's task
        3. Should fail with 404 (task not found for this user)
        """
        # Create second user
        client.post(
            "/auth/signup",
            json={
                "username": "user2",
                "email": "user2@example.com",
                "password": "password123"
            }
        )
        
        # Login as second user
        login_response = client.post(
            "/auth/login",
            data={"username": "user2", "password": "password123"}
        )
        user2_token = login_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # User 2 tries to delete User 1's task
        response = client.delete(
            f"/tasks/{test_task['id']}", 
            headers=user2_headers
        )
        
        # Should be 404 because task doesn't belong to User 2
        assert response.status_code == status.HTTP_404_NOT_FOUND
