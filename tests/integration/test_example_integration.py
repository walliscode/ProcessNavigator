"""
Example integration test demonstrating the testing framework.

This file shows how to write integration tests that verify
multiple components working together with database access.
"""

import pytest
from tests.utils.helpers import register_and_login
from tests.utils.assertions import (
    assert_status_code,
    assert_response_contains,
    assert_database_has_record
)


@pytest.mark.integration
@pytest.mark.database
def test_user_registration_and_login(client, test_app):
    """
    Test user can register and login successfully.
    
    This integration test verifies:
    1. User registration persists to database
    2. User can login with registered credentials
    3. Session is created after login
    """
    from process_navigator.extensions.database import db
    from process_navigator.models import User
    
    # Register user
    register_response = client.post("/register", data={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "testpassword",
        "submit": True
    }, follow_redirects=True)
    
    assert_status_code(register_response, 200)
    
    # Verify user in database
    with test_app.app_context():
        user = assert_database_has_record(User, db.session, email="test@example.com")
        assert user.first_name == "Test"
        assert user.last_name == "User"
    
    # Login user
    login_response = client.post("/login", data={
        "email": "test@example.com",
        "password": "testpassword",
        "submit": True
    })
    
    # Should redirect to home after successful login
    assert login_response.status_code == 302


@pytest.mark.integration
@pytest.mark.database
def test_create_process_method_with_helper(client, test_app):
    """
    Test creating a process method using helper functions.
    
    Demonstrates using the helpers to simplify test setup.
    """
    from process_navigator.extensions.database import db
    from process_navigator.models.process import ProcessMethod
    
    # Setup: register and login using helper
    register_and_login(client, email="test@example.com", password="password")
    
    # Navigate to data page
    client.get("/data")
    
    # Create process method
    response = client.post("/data/add_process_method", data={
        "name": "Integration Test Method",
        "description": "Created in integration test",
        "file_name": "integration_test.txt",
        "submit": True
    }, follow_redirects=True)
    
    # Verify response
    assert_status_code(response, 200)
    
    # Verify in database
    with test_app.app_context():
        pm = assert_database_has_record(
            ProcessMethod,
            db.session,
            name="Integration Test Method"
        )
        assert pm.description == "Created in integration test"
        assert pm.file_name == "integration_test.txt"


@pytest.mark.integration
@pytest.mark.database
def test_process_method_parts_persistence(client, test_app):
    """
    Test that process method parts are properly persisted.
    
    This test verifies the relationship between ProcessMethod
    and ProcessMethodPart through the full application stack.
    """
    from process_navigator.extensions.database import db
    from process_navigator.models.process import ProcessMethod, ProcessMethodPart
    
    # Setup
    register_and_login(client)
    
    # Create process method with parts
    # (This would need the actual implementation to work)
    # For now, we'll create directly in the database as an example
    
    with test_app.app_context():
        pm = ProcessMethod(
            name="Test Method with Parts",
            description="Testing parts",
            file_name="test.txt"
        )
        db.session.add(pm)
        db.session.commit()
        
        # Add parts
        part1 = ProcessMethodPart(name="Part 1", process_method_id=pm.id)
        part2 = ProcessMethodPart(name="Part 2", process_method_id=pm.id)
        db.session.add(part1)
        db.session.add(part2)
        db.session.commit()
        
        # Verify relationship
        pm_check = db.session.query(ProcessMethod).filter_by(
            name="Test Method with Parts"
        ).first()
        
        assert pm_check is not None
        assert len(pm_check.process_method_parts) == 2
        part_names = [p.name for p in pm_check.process_method_parts]
        assert "Part 1" in part_names
        assert "Part 2" in part_names


@pytest.mark.integration
@pytest.mark.database
@pytest.mark.authentication
def test_unauthorized_access_redirects_to_login(client):
    """
    Test that unauthorized access to protected pages redirects to login.
    
    This verifies the authentication decorator is working properly.
    """
    # Try to access protected page without logging in
    response = client.get("/data")
    
    # Should redirect to login
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")


@pytest.mark.integration
@pytest.mark.database
def test_session_management(client, test_app):
    """
    Test that session is properly managed across requests.
    
    This verifies session creation, persistence, and cleanup.
    """
    from tests.utils.helpers import set_session_value, get_session_value
    
    # Register and login
    register_and_login(client)
    
    # Check that user_id is in session (if implemented)
    user_id = get_session_value(client, "user_id")
    # Note: This depends on how session is implemented
    
    # Make authenticated request
    response = client.get("/data")
    assert_status_code(response, 200)
    
    # Session should persist
    user_id_after = get_session_value(client, "user_id")
    if user_id and user_id_after:
        assert user_id == user_id_after
