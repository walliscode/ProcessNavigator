# System Tests (End-to-End)

This directory contains system tests for ProcessNavigator.

## Purpose

System tests verify complete user workflows from start to finish. They:
- Test real user scenarios
- Verify multi-step processes
- Test critical business workflows
- Validate complete application stack

## What to Test

- Complete user journeys (registration → process creation → analysis)
- Multi-page workflows
- Authentication and authorization flows
- Critical business processes
- Error recovery scenarios
- User interactions across multiple features

## Organization

Tests are organized by workflow type:
- `test_user_journeys.py`: Complete user workflows
- `test_process_workflows.py`: Process creation and execution workflows
- `test_error_scenarios.py`: Error handling and recovery

## Running System Tests

```bash
# Run all system tests
pytest tests/system/ -v

# Run specific test file
pytest tests/system/test_user_journeys.py

# Run with marker
pytest -m system

# Exclude slow tests during development
pytest -m "system and not slow"
```

## Example Test

```python
import pytest
from tests.utils.helpers import provide_stacked_response
from tests.utils.assertions import assert_status_code, assert_response_contains

@pytest.mark.system
@pytest.mark.slow
@pytest.mark.critical
def test_complete_process_creation_journey(client, route_options):
    """
    Test complete user journey from registration to process creation.
    
    This test verifies that a user can:
    1. Register a new account
    2. Log in
    3. Navigate to data management
    4. Create a new process method
    5. View the created process method
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
    assert_response_contains(response, "Add Process Method")
```

## Best Practices

1. **Test Real Scenarios**: Use realistic user workflows
2. **Document Purpose**: Explain what business process is being tested
3. **Mark as Slow**: Use @pytest.mark.slow for tests >5 seconds
4. **Mark as Critical**: Use @pytest.mark.critical for essential workflows
5. **Keep Manageable**: Don't test every possible path, focus on critical ones
6. **Use Helpers**: Use `provide_stacked_response` for sequential actions
7. **Meaningful Assertions**: Verify key outcomes, not every detail
