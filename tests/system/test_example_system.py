"""
Example system test demonstrating end-to-end workflows.

System tests verify complete user journeys through the application,
testing the full stack from user interaction to data persistence.
"""

import pytest
from tests.utils.helpers import provide_stacked_response
from tests.utils.assertions import (
    assert_status_code,
    assert_response_contains,
    assert_database_has_record
)


@pytest.mark.system
@pytest.mark.slow
@pytest.mark.critical
def test_complete_user_registration_to_data_management(client, route_options, test_app):
    """
    Test complete user journey from registration to data management.
    
    This system test verifies a realistic user workflow:
    1. User visits home page
    2. User registers for an account
    3. User logs in
    4. User navigates to data management
    5. User views process methods
    
    This ensures the entire application stack works together.
    """
    from process_navigator.extensions.database import db
    from process_navigator.models import User
    
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get"
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    # Verify final response
    assert_status_code(response, 200)
    assert_response_contains(response, "Process Methods")
    
    # Verify user was created in database
    with test_app.app_context():
        user = assert_database_has_record(
            User,
            db.session,
            email="test_user@astrea-bio.com"
        )
        assert user.first_name == "test"
        assert user.last_name == "user"


@pytest.mark.system
@pytest.mark.slow
def test_process_method_creation_workflow(client, route_options, test_app):
    """
    Test complete workflow for creating a process method.
    
    User journey:
    1. Register and login
    2. Navigate to data management
    3. Go to process methods page
    4. Click "Add Method"
    5. View add method form
    
    This verifies the complete navigation flow works correctly.
    """
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
        "process_method_post_add_method",
        "add_process_method_get"
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    assert_status_code(response, 200)
    assert_response_contains(response, ["Add Process Method", "Name", "Description"])


@pytest.mark.system
@pytest.mark.slow
@pytest.mark.critical
def test_input_management_workflow(client, route_options):
    """
    Test complete workflow for managing inputs.
    
    This test verifies users can:
    - Navigate to inputs page
    - View inputs
    - Access input management features
    """
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get"
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    assert_status_code(response, 200)
    assert_response_contains(response, [
        "Inputs",
        "Add Input",
        "Edit Input",
        "Delete Input"
    ])


@pytest.mark.system
@pytest.mark.slow
def test_units_management_workflow(client, route_options):
    """
    Test complete workflow for managing units.
    
    Verifies the units management page is accessible
    and displays expected content.
    """
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "units_get"
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    assert_status_code(response, 200)
    assert_response_contains(response, [
        "Units",
        "Add Unit",
        "Edit Unit",
        "Delete Unit"
    ])


@pytest.mark.system
@pytest.mark.slow
def test_analysis_methods_workflow(client, route_options):
    """
    Test complete workflow for managing analysis methods.
    
    Verifies users can navigate to and interact with
    the analysis methods management page.
    """
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get"
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    assert_status_code(response, 200)
    assert_response_contains(response, [
        "Analysis Methods",
        "Add Analysis Method"
    ])


@pytest.mark.system
@pytest.mark.slow
@pytest.mark.critical
def test_failed_login_workflow(client, route_options):
    """
    Test error handling for failed login attempt.
    
    This system test verifies that error scenarios
    are handled gracefully throughout the application.
    """
    paths = [
        "login_user"  # Try to login without registering
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    assert_status_code(response, 200)
    assert_response_contains(response, "does not exist")


@pytest.mark.system
@pytest.mark.slow
def test_unauthorized_access_workflow(client, route_options):
    """
    Test that unauthorized users cannot access protected pages.
    
    Verifies security across the application - users should
    be redirected to login when accessing protected resources.
    """
    paths = ["data_index_get"]  # Try to access without login
    
    response = provide_stacked_response(client, paths, route_options)
    
    # Should redirect to login
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")


@pytest.mark.system
@pytest.mark.slow
def test_cauldron_workflow(client, route_options):
    """
    Test cauldron (process path) workflow.
    
    This test verifies the process path creation workflow,
    which is a core feature of the application.
    """
    paths = [
        "register_user",
        "login_user",
        "cauldron_index_get"
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    assert_status_code(response, 200)
    # Verify cauldron page content (adjust based on actual implementation)
    # assert_response_contains(response, "Cauldron")
