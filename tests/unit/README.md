# Unit Tests

This directory contains unit tests for ProcessNavigator.

## Purpose

Unit tests verify individual functions, methods, and classes in isolation. They should:
- Run quickly (<100ms per test)
- Not access the database (use mocks)
- Not make network calls
- Not perform file I/O (mock filesystem)

## What to Test

- Model class instantiation and methods
- Model properties and hybrid properties
- Utility functions
- Form validators
- Data transformations
- Business logic calculations
- Helper functions

## Organization

Tests are organized by module:
- `test_models_*.py`: Tests for database models
- `test_utils.py`: Tests for utility functions
- `test_decorators.py`: Tests for custom decorators
- `test_forms.py`: Tests for form validators

## Running Unit Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_models_process.py

# Run with marker
pytest -m unit
```

## Example Test

```python
import pytest
from process_navigator.models.process import ProcessMethod

@pytest.mark.unit
def test_process_method_creation():
    """Test ProcessMethod can be instantiated with valid data"""
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    
    assert pm.name == "Test Method"
    assert pm.description == "Test Description"
    assert pm.file_name == "test.txt"
```

## Best Practices

1. **Mock External Dependencies**: Use mocks for database, file system, network
2. **Test One Thing**: Each test should verify one behavior
3. **Use Descriptive Names**: Test names should explain what is being tested
4. **Keep Tests Fast**: Unit tests should execute in milliseconds
5. **Avoid Setup Complexity**: Minimal setup per test
