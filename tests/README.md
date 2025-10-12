# ProcessNavigator Testing Suite

Welcome to the ProcessNavigator testing suite! This directory contains a comprehensive, data-driven testing framework designed to support the project throughout its lifetime.

## Quick Start

```bash
# Run all tests
pytest

# Run tests by level
pytest tests/unit/          # Fast unit tests
pytest tests/integration/   # Integration tests
pytest tests/system/        # End-to-end tests

# Run by marker
pytest -m unit             # Only unit tests
pytest -m "not slow"       # Exclude slow tests
pytest -m critical         # Only critical tests

# Run with coverage
pytest --cov=process_navigator --cov-report=html
```

## Documentation

- **[TESTING_FRAMEWORK.md](../TESTING_FRAMEWORK.md)** - Complete framework documentation
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Guide for migrating existing tests
- **[utils/](utils/)** - Reusable test utilities
- **Level-specific READMEs**: See each test directory for detailed information

## Directory Structure

```
tests/
├── README.md                    # This file
├── MIGRATION_GUIDE.md           # Migration guide
├── pytest.ini                   # Pytest configuration
├── conftest.py                  # Global fixtures
│
├── unit/                        # Unit tests (fast, isolated)
│   ├── README.md
│   ├── test_models_*.py        # Model tests
│   ├── test_utils.py           # Utility function tests
│   └── test_decorators.py      # Decorator tests
│
├── integration/                 # Integration tests (database access)
│   ├── README.md
│   ├── test_home_routes.py     # Home/auth routes
│   ├── test_data_routes.py     # Data management routes
│   ├── test_cauldron_routes.py # Cauldron routes
│   └── test_database_relationships.py
│
├── system/                      # System tests (end-to-end)
│   ├── README.md
│   ├── test_user_journeys.py   # Complete user workflows
│   └── test_process_workflows.py
│
├── performance/                 # Performance tests
│   ├── README.md
│   └── test_query_performance.py
│
├── utils/                       # Test utilities
│   ├── __init__.py
│   ├── assertions.py           # Custom assertion helpers
│   ├── factories.py            # Test data factories
│   ├── generators.py           # Data generators
│   └── helpers.py              # General helpers
│
├── fixtures/                    # Fixture modules
│   └── __init__.py
│
├── data/                        # Test data files
│   ├── route_options.json      # HTTP request definitions
│   ├── user_paths.json         # User journey definitions
│   ├── test_data.json          # Database seed data
│   ├── scenarios/              # Scenario-specific data
│   │   ├── edge_cases.json
│   │   └── large_dataset.json
│   └── schema/                 # JSON schemas
│       ├── route_options_schema.json
│       └── test_data_schema.json
│
├── load_data.py                # Database loading utilities
└── utils.py                    # Legacy utilities (being phased out)
```

## Test Levels

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual functions and classes in isolation
- **Speed**: <100ms per test
- **Database**: No (use mocks)
- **Coverage**: 70-80% of all tests

### Integration Tests (`tests/integration/`)
- **Purpose**: Test components working together
- **Speed**: 1-5 seconds per test
- **Database**: Yes (test database)
- **Coverage**: 15-25% of all tests

### System Tests (`tests/system/`)
- **Purpose**: Test complete user workflows
- **Speed**: 5-30 seconds per test
- **Database**: Yes (full application)
- **Coverage**: 5-10% of all tests

### Performance Tests (`tests/performance/`)
- **Purpose**: Verify performance requirements
- **Speed**: Varies (often slow)
- **Database**: Yes (large datasets)
- **Coverage**: As needed

## Key Features

### Data-Driven Testing

Tests are driven by JSON data files, making it easy to add test cases:

```python
# Define routes in route_options.json
{
  "name": "login_user",
  "route": "/login",
  "method": "POST",
  "data": {"email": "test@example.com", "password": "password"}
}

# Use in tests
response = provide_stacked_response(client, ["register_user", "login_user"], route_options)
```

### Reusable Utilities

Comprehensive utilities for common testing needs:

```python
from tests.utils.assertions import assert_database_has_record
from tests.utils.factories import ProcessMethodFactory
from tests.utils.helpers import register_and_login

# Use factories to create test data
pm = ProcessMethodFactory.create(db_session, name="Custom Name")

# Use assertions for clear error messages
assert_database_has_record(ProcessMethod, db_session, name="Custom Name")

# Use helpers for common operations
register_and_login(client, email="test@example.com")
```

### Test Markers

Organize and filter tests with markers:

```python
@pytest.mark.unit
@pytest.mark.fast
def test_model_creation():
    pass

@pytest.mark.integration
@pytest.mark.database
def test_route_handler():
    pass

@pytest.mark.system
@pytest.mark.slow
@pytest.mark.critical
def test_user_journey():
    pass
```

## Writing Tests

### Unit Test Example

```python
import pytest
from process_navigator.models.process import ProcessMethod

@pytest.mark.unit
def test_process_method_creation():
    """Test ProcessMethod can be instantiated."""
    pm = ProcessMethod(name="Test", description="Desc", file_name="file.txt")
    assert pm.name == "Test"
```

### Integration Test Example

```python
import pytest
from tests.utils.helpers import register_and_login
from tests.utils.assertions import assert_database_has_record

@pytest.mark.integration
@pytest.mark.database
def test_create_process_method(client, test_app):
    """Test creating process method persists to database."""
    register_and_login(client)
    
    response = client.post("/data/add_process_method", data={
        "name": "New Method",
        "description": "Test",
        "submit": True
    })
    
    with test_app.app_context():
        from process_navigator.extensions.database import db
        from process_navigator.models.process import ProcessMethod
        assert_database_has_record(ProcessMethod, db.session, name="New Method")
```

### System Test Example

```python
import pytest
from tests.utils.helpers import provide_stacked_response

@pytest.mark.system
@pytest.mark.slow
def test_complete_workflow(client, route_options):
    """Test complete user workflow."""
    paths = ["register_user", "login_user", "data_index_get", "process_method_get"]
    response = provide_stacked_response(client, paths, route_options)
    assert response.status_code == 200
```

## Common Tasks

### Adding a New Test

1. Determine test level (unit, integration, system)
2. Create test in appropriate directory
3. Add necessary markers
4. Use utilities for common operations
5. Follow naming convention: `test_<component>_<action>_<expected>`

### Adding Test Data

1. For database seed data: Edit `tests/data/test_data.json`
2. For HTTP requests: Edit `tests/data/route_options.json`
3. For user journeys: Edit `tests/data/user_paths.json`
4. For scenarios: Create file in `tests/data/scenarios/`

### Running Specific Tests

```bash
# Run specific file
pytest tests/unit/test_models_process.py

# Run specific test
pytest tests/unit/test_models_process.py::test_process_method_creation

# Run by keyword
pytest -k "process_method"

# Run marked tests
pytest -m "integration and database"
pytest -m "not slow"
```

### Debugging Tests

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l
```

## Best Practices

1. **Independence**: Tests should not depend on each other
2. **Clarity**: Use descriptive names and docstrings
3. **Speed**: Keep unit tests fast; mark slow tests
4. **Reusability**: Use factories and helpers
5. **Data-Driven**: Define test data in JSON files
6. **Assertions**: Use custom assertions for better messages
7. **Coverage**: Aim for >80% code coverage
8. **Documentation**: Document complex test scenarios

## Continuous Improvement

The testing framework is designed to evolve:

- **Phase 1** (Current): Foundation with unit, integration, system tests
- **Phase 2**: Add performance testing, parallel execution
- **Phase 3**: UI testing, API testing, security testing
- **Phase 4**: CI/CD integration, automated reporting

## Getting Help

- Review [TESTING_FRAMEWORK.md](../TESTING_FRAMEWORK.md) for comprehensive documentation
- Check example tests in each directory
- Review [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for migrating existing tests
- Consult [pytest documentation](https://docs.pytest.org/)

## Contributing

When adding tests:

1. Follow the established patterns
2. Use appropriate test level and markers
3. Add documentation for complex scenarios
4. Keep tests maintainable and readable
5. Update test data files as needed

## Performance Targets

Based on project requirements:
- **Test Execution**: <5 minutes for full suite
- **Unit Tests**: <1 second per test
- **Integration Tests**: <5 seconds per test
- **Coverage**: >80% code coverage
- **Flakiness**: <1% flaky tests

## Support

For questions or issues with the testing framework:
1. Review the documentation
2. Check existing tests for examples
3. Ask in team meetings
4. Update documentation when you find gaps
