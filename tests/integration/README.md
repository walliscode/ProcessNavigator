# Integration Tests

This directory contains integration tests for ProcessNavigator.

## Purpose

Integration tests verify that multiple components work together correctly. They:
- Test interactions between components
- Access the test database
- Test routes with database operations
- Verify form submissions persist data
- Test model relationships

## What to Test

- Route handlers with database operations
- Form submissions with persistence
- Model relationships and cascading
- Session management
- File upload and storage
- Authentication flows
- Query operations

## Organization

Tests are organized by feature area:
- `test_home_routes.py`: User registration, login, home page
- `test_data_routes.py`: Data management routes (inputs, parameters, etc.)
- `test_cauldron_routes.py`: Process path creation and management
- `test_database_relationships.py`: Model relationships and cascading

## Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/integration/test_data_routes.py

# Run with marker
pytest -m integration
```

## Example Test

```python
import pytest
from tests.utils.helpers import register_and_login
from tests.utils.assertions import assert_database_has_record
from process_navigator.models.process import ProcessMethod

@pytest.mark.integration
@pytest.mark.database
def test_create_process_method(client, test_app):
    """Test creating a process method persists to database"""
    # Setup: register and login user
    register_and_login(client, email="test@example.com", password="password")
    
    # Action: create process method
    response = client.post("/data/add_process_method", data={
        "name": "New Method",
        "description": "Test Description",
        "submit": True
    })
    
    # Assert: verify in database
    with test_app.app_context():
        from process_navigator.extensions.database import db
        assert_database_has_record(
            ProcessMethod, 
            db.session, 
            name="New Method"
        )
```

## Best Practices

1. **Use Test Database**: Always use test configuration
2. **Clean State**: Each test should start with clean database state
3. **Test Real Interactions**: Don't mock database or core components
4. **Verify Persistence**: Check that data is actually saved
5. **Test Error Cases**: Test validation failures and error handling
