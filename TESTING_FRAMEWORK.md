# ProcessNavigator Testing Framework

## Overview

This document defines a comprehensive, data-driven testing framework for ProcessNavigator that supports the project's lifetime. The framework is designed for reusability, maintainability, and scalability, with clear separation between unit, integration, and system tests.

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Levels](#test-levels)
3. [Framework Architecture](#framework-architecture)
4. [Directory Structure](#directory-structure)
5. [Data-Driven Testing Approach](#data-driven-testing-approach)
6. [Fixtures and Utilities](#fixtures-and-utilities)
7. [Test Organization](#test-organization)
8. [Best Practices](#best-practices)
9. [Getting Started](#getting-started)
10. [Future Enhancements](#future-enhancements)

---

## Testing Philosophy

### Core Principles

1. **Data-Driven**: Tests are driven by JSON data files, making it easy to add new test cases without code changes
2. **Reusable**: Common patterns are extracted into fixtures and utilities
3. **Maintainable**: Clear organization and naming conventions make tests easy to understand and modify
4. **Comprehensive**: Coverage across unit, integration, and system levels
5. **Fast**: Unit tests run quickly; slower integration/system tests are clearly marked
6. **Isolated**: Tests don't depend on each other and can run in any order
7. **Realistic**: Test data reflects real-world scenarios

### Testing Goals

- **Coverage Target**: >80% code coverage
- **Test Execution Time**: 
  - Unit tests: <1 second per test
  - Integration tests: <5 seconds per test
  - System tests: <30 seconds per test
- **Data-Driven Coverage**: All critical user paths defined in JSON
- **Regression Protection**: All bugs get a test before being fixed

---

## Test Levels

### 1. Unit Tests

**Purpose**: Test individual functions, methods, and classes in isolation

**Characteristics**:
- No database access (use mocks/stubs)
- No network calls
- No file I/O (mock filesystem)
- Fast execution (<100ms per test)
- High volume (70-80% of all tests)

**What to Test**:
- Model methods and properties
- Utility functions
- Form validators
- Data transformations
- Business logic calculations

**Example Structure**:
```python
# tests/unit/test_models.py
def test_process_method_part_creation():
    """Test ProcessMethodPart can be instantiated with valid data"""
    
def test_unit_combination_symbol_generation():
    """Test Unit correctly generates compound symbols"""
    
def test_path_data_expansion_single_input():
    """Test PathData expands correctly with single input"""
```

### 2. Integration Tests

**Purpose**: Test interactions between components

**Characteristics**:
- Database access (test database)
- Multiple components working together
- Moderate execution time (1-5 seconds)
- Medium volume (15-25% of all tests)

**What to Test**:
- Route handlers with database operations
- Form submissions with database persistence
- Model relationships and cascading
- Session management
- File upload and storage
- Query performance

**Example Structure**:
```python
# tests/integration/test_data_routes.py
def test_create_process_method_with_parts(client, test_app):
    """Test complete workflow of creating process method with parts"""
    
def test_input_deletion_cascade(client, test_app):
    """Test that deleting input cascades correctly to related entities"""
    
def test_process_path_expansion(client, test_app):
    """Test that process paths expand correctly with multiple inputs"""
```

### 3. System Tests (End-to-End)

**Purpose**: Test complete user workflows from start to finish

**Characteristics**:
- Full application stack
- Real user scenarios
- Slower execution (5-30 seconds)
- Lower volume (5-10% of all tests)

**What to Test**:
- Complete user journeys
- Multi-page workflows
- Authentication flows
- Critical business processes
- User error scenarios

**Example Structure**:
```python
# tests/system/test_user_journeys.py
def test_complete_process_path_creation_journey(client, route_options):
    """Test user can register, login, create process, and generate paths"""
    
def test_experiment_tracking_workflow(client, route_options):
    """Test complete workflow from process definition to result analysis"""
```

### 4. Performance Tests

**Purpose**: Ensure application meets performance requirements

**Characteristics**:
- Large data volumes
- Concurrent users (if applicable)
- Response time measurements
- Resource usage monitoring

**What to Test**:
- Query performance with large datasets
- Page load times
- Path expansion with many combinations
- Concurrent user operations

---

## Framework Architecture

### Component Overview

```
Testing Framework
├── Test Data Layer (JSON files)
│   ├── route_options.json    # HTTP request definitions
│   ├── user_paths.json        # User journey definitions
│   ├── test_data.json         # Database seed data
│   └── test_scenarios/        # Scenario-specific data
├── Data Validation Layer (JSON schemas)
│   └── Ensures test data integrity
├── Fixture Layer (conftest.py)
│   ├── Application fixtures
│   ├── Database fixtures
│   ├── Data loading fixtures
│   └── Utility fixtures
├── Utility Layer (utils/)
│   ├── Test helpers
│   ├── Data generators
│   ├── Assertion helpers
│   └── Mock factories
└── Test Layer (test_*.py)
    ├── Unit tests
    ├── Integration tests
    └── System tests
```

### Data Flow

```
JSON Test Data → Schema Validation → Fixture Loading → Test Execution → Assertions
                                    ↓
                              Database Setup
                              Mock Configuration
```

---

## Directory Structure

### Proposed Structure

```
tests/
├── __init__.py
├── conftest.py                      # Global fixtures
├── pytest.ini                       # Pytest configuration
│
├── unit/                           # Unit tests
│   ├── __init__.py
│   ├── conftest.py                 # Unit-specific fixtures
│   ├── test_models_process.py
│   ├── test_models_units.py
│   ├── test_models_inputs.py
│   ├── test_models_parameters.py
│   ├── test_models_analysis.py
│   ├── test_cauldron_models.py
│   ├── test_utils.py
│   ├── test_decorators.py
│   └── test_forms.py
│
├── integration/                    # Integration tests
│   ├── __init__.py
│   ├── conftest.py                 # Integration-specific fixtures
│   ├── test_home_routes.py
│   ├── test_data_routes.py
│   ├── test_cauldron_routes.py
│   ├── test_database_relationships.py
│   └── test_session_management.py
│
├── system/                         # System/E2E tests
│   ├── __init__.py
│   ├── conftest.py                 # System-specific fixtures
│   ├── test_user_journeys.py
│   ├── test_process_workflows.py
│   └── test_error_scenarios.py
│
├── performance/                    # Performance tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_query_performance.py
│   └── test_load_handling.py
│
├── data/                          # Test data files
│   ├── route_options.json         # HTTP endpoints and request data
│   ├── user_paths.json            # User journey definitions
│   ├── test_data.json             # Database seed data
│   ├── scenarios/                 # Scenario-specific data
│   │   ├── large_dataset.json
│   │   ├── complex_paths.json
│   │   └── edge_cases.json
│   ├── schema/                    # JSON schemas for validation
│   │   ├── route_options_schema.json
│   │   ├── user_paths_schema.json
│   │   └── test_data_schema.json
│   └── test_files/                # Files for upload testing
│
├── utils/                         # Test utilities
│   ├── __init__.py
│   ├── assertions.py              # Custom assertion helpers
│   ├── factories.py               # Test data factories
│   ├── generators.py              # Data generators
│   ├── mocks.py                   # Mock objects and factories
│   └── helpers.py                 # General test helpers
│
├── load_data.py                   # Database loading utilities
└── fixtures/                      # Fixture modules
    ├── __init__.py
    ├── app_fixtures.py
    ├── database_fixtures.py
    ├── data_fixtures.py
    └── mock_fixtures.py
```

### Migration from Current Structure

**Current Structure** → **New Structure**:
- `test_home_routes.py` → `integration/test_home_routes.py`
- `test_data_routes.py` → `integration/test_data_routes.py`
- `test_cauldron_routes.py` → `integration/test_cauldron_routes.py`
- `test_data.py` → `integration/test_database_relationships.py`
- Extract unit tests from route tests → `unit/test_models_*.py`

---

## Data-Driven Testing Approach

### Core Concept

Tests are driven by declarative JSON data files, allowing non-developers to add test cases and making tests more maintainable.

### Route Options (HTTP Requests)

**File**: `tests/data/route_options.json`

**Purpose**: Define all HTTP requests used in tests

**Structure**:
```json
{
  "name": "login_user",
  "route": "/login",
  "method": "POST",
  "data": {
    "email": "test_user@astrea-bio.com",
    "password": "testpassword",
    "submit": true
  },
  "expected_status": 302,
  "expected_redirect": "/",
  "tags": ["authentication", "critical"]
}
```

**Enhanced Fields**:
- `expected_status`: Expected HTTP status code
- `expected_redirect`: Expected redirect location (for 302 responses)
- `tags`: Categories for filtering tests
- `depends_on`: Routes that must succeed first
- `timeout`: Maximum execution time
- `validate_response`: List of expected content

### User Paths (User Journeys)

**File**: `tests/data/user_paths.json`

**Purpose**: Define complete user journeys as sequences of route actions

**Structure**:
```json
{
  "name": "complete_process_creation",
  "description": "User creates a complete process from scratch",
  "category": "critical",
  "path": [
    "register_user",
    "login_user",
    "data_index_get",
    "process_method_get",
    "process_method_post_add_method",
    "add_process_method_get"
  ],
  "expected_final_state": {
    "session_keys": ["user_id", "process_method_id"],
    "database_changes": {
      "ProcessMethod": 1
    }
  },
  "cleanup": ["delete_process_method"]
}
```

**Enhanced Fields**:
- `category`: critical, important, nice-to-have
- `expected_final_state`: Expected application state after journey
- `cleanup`: Routes to call for test cleanup
- `preconditions`: Required system state
- `postconditions`: Expected system state

### Test Data (Database Seeds)

**File**: `tests/data/test_data.json`

**Purpose**: Define database seed data for tests

**Current Structure**: Working well, but can be enhanced with:

```json
{
  "ProcessMethods": [...],
  "BaseUnits": [...],
  "scenarios": {
    "minimal": {
      "ProcessMethods": [...],
      "description": "Minimal data for basic tests"
    },
    "complex": {
      "ProcessMethods": [...],
      "description": "Complex data for advanced scenarios"
    },
    "large_scale": {
      "ProcessMethods": [...],
      "description": "Large dataset for performance testing"
    }
  }
}
```

**Benefits**:
- Different test levels can use appropriate data volumes
- Performance tests can use realistic large datasets
- Reduces test execution time for simple tests

### Test Scenarios

**Location**: `tests/data/scenarios/`

**Purpose**: Scenario-specific data files for edge cases and special situations

**Examples**:
- `edge_cases.json`: Boundary values, null handling, empty sets
- `error_scenarios.json`: Invalid data, constraint violations
- `complex_workflows.json`: Multi-step processes with many variations
- `large_dataset.json`: Thousands of records for performance testing

---

## Fixtures and Utilities

### Core Fixtures (Global)

Located in `tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def app_config():
    """Application configuration for testing"""
    
@pytest.fixture
def test_app():
    """Flask application instance with test configuration"""
    
@pytest.fixture
def client(test_app):
    """Flask test client for making requests"""
    
@pytest.fixture
def db_session(test_app):
    """Database session with automatic rollback"""
    
@pytest.fixture(scope="session")
def route_options():
    """Load route options from JSON"""
    
@pytest.fixture(scope="session")
def user_paths():
    """Load user paths from JSON"""
    
@pytest.fixture
def authenticated_client(client, route_options):
    """Pre-authenticated test client"""
```

### Level-Specific Fixtures

#### Unit Test Fixtures (`tests/unit/conftest.py`)

```python
@pytest.fixture
def mock_db_session():
    """Mock database session for unit tests"""
    
@pytest.fixture
def sample_process_method():
    """Sample ProcessMethod object (not persisted)"""
    
@pytest.fixture
def sample_user():
    """Sample User object (not persisted)"""
```

#### Integration Test Fixtures (`tests/integration/conftest.py`)

```python
@pytest.fixture
def db_with_test_data(test_app):
    """Database populated with full test data"""
    
@pytest.fixture
def db_with_minimal_data(test_app):
    """Database with minimal test data for faster tests"""
    
@pytest.fixture
def temp_file_storage():
    """Temporary file storage for upload tests"""
```

#### System Test Fixtures (`tests/system/conftest.py`)

```python
@pytest.fixture
def browser_client():
    """Selenium browser client for UI testing (future)"""
    
@pytest.fixture
def complete_application_state(test_app):
    """Application with all components initialized"""
```

### Utility Functions

#### Assertion Helpers (`tests/utils/assertions.py`)

```python
def assert_response_contains(response, expected_content):
    """Assert response contains expected HTML/JSON content"""
    
def assert_database_count(model, expected_count, db_session):
    """Assert database has expected record count"""
    
def assert_session_keys(client, expected_keys):
    """Assert session has expected keys"""
    
def assert_redirects_to(response, expected_location):
    """Assert response redirects to expected location"""
    
def assert_flash_message(response, expected_message):
    """Assert flash message is present in response"""
```

#### Data Factories (`tests/utils/factories.py`)

```python
class ProcessMethodFactory:
    """Factory for creating ProcessMethod test objects"""
    
    @staticmethod
    def create(**kwargs):
        """Create ProcessMethod with default or custom values"""
        
    @staticmethod
    def create_batch(count, **kwargs):
        """Create multiple ProcessMethods"""
        
class UserFactory:
    """Factory for creating User test objects"""
    
class InputFactory:
    """Factory for creating Input test objects"""
```

#### Data Generators (`tests/utils/generators.py`)

```python
def generate_process_methods(count, with_parts=True):
    """Generate process methods with realistic data"""
    
def generate_user_paths(complexity="simple"):
    """Generate user path scenarios"""
    
def generate_large_dataset(tables, records_per_table):
    """Generate large datasets for performance testing"""
```

#### Test Helpers (`tests/utils/helpers.py`)

```python
def provide_stacked_response(client, paths, route_options):
    """Execute sequence of requests and return final response"""
    
def login_user(client, email, password):
    """Helper to log in a user"""
    
def create_process_method(client, **kwargs):
    """Helper to create a process method"""
    
def cleanup_database(db_session, tables):
    """Clean up specific database tables"""
```

### Parametrization Support

```python
# tests/data/scenarios/parameter_tests.json
{
  "unit_conversions": [
    {
      "input": {"value": 1, "unit": "kg"},
      "expected": {"value": 1000, "unit": "g"}
    },
    {
      "input": {"value": 1, "unit": "m"},
      "expected": {"value": 100, "unit": "cm"}
    }
  ]
}

# tests/unit/test_unit_conversions.py
import pytest
from tests.utils.helpers import load_test_scenarios

@pytest.mark.parametrize(
    "test_case",
    load_test_scenarios("parameter_tests.json")["unit_conversions"]
)
def test_unit_conversion(test_case):
    result = convert_unit(test_case["input"])
    assert result == test_case["expected"]
```

---

## Test Organization

### Naming Conventions

#### Test Files
- Unit tests: `test_models_<module>.py`, `test_utils_<module>.py`
- Integration tests: `test_<blueprint>_routes.py`, `test_<feature>.py`
- System tests: `test_<user_journey>.py`, `test_<workflow>.py`

#### Test Functions
```python
# Pattern: test_<component>_<action>_<expected_result>

# Unit test examples
def test_process_method_creation_with_valid_data():
def test_unit_symbol_generation_for_compound_units():
def test_path_expansion_raises_error_with_invalid_input():

# Integration test examples
def test_login_route_redirects_to_home_on_success():
def test_create_process_method_persists_to_database():
def test_delete_input_cascades_to_dependent_records():

# System test examples
def test_user_can_complete_full_registration_and_login_flow():
def test_user_can_create_process_and_generate_paths():
```

### Test Markers

Use pytest markers to categorize and filter tests:

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (database access)
    system: System tests (end-to-end)
    performance: Performance tests (slow)
    smoke: Smoke tests (critical functionality)
    slow: Slow tests (>5 seconds)
    database: Tests requiring database
    authentication: Authentication-related tests
    critical: Critical business functionality

# Example usage
@pytest.mark.unit
@pytest.mark.fast
def test_model_creation():
    pass

@pytest.mark.integration
@pytest.mark.database
def test_database_query():
    pass

@pytest.mark.system
@pytest.mark.slow
def test_complete_workflow():
    pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific levels
pytest tests/unit/
pytest tests/integration/
pytest tests/system/

# Run by marker
pytest -m unit                  # Only unit tests
pytest -m "integration and database"
pytest -m "not slow"           # Exclude slow tests
pytest -m critical             # Only critical tests

# Run specific test file
pytest tests/unit/test_models_process.py

# Run specific test
pytest tests/unit/test_models_process.py::test_process_method_creation

# Run with coverage
pytest --cov=process_navigator --cov-report=html

# Run in parallel (install pytest-xdist)
pytest -n auto

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

---

## Best Practices

### 1. Test Independence

**Do**:
- Each test should be able to run independently
- Use fixtures for setup and teardown
- Don't rely on test execution order

**Don't**:
- Share state between tests
- Depend on side effects from other tests

```python
# Good
def test_create_user(client, db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    assert db_session.query(User).count() == 1

# Bad - depends on previous test
def test_user_count():
    assert db_session.query(User).count() == 1  # Assumes user exists
```

### 2. Test Data Management

**Do**:
- Use factories for creating test data
- Use JSON files for scenario data
- Clear data between tests

**Don't**:
- Hardcode test data in test functions
- Reuse test data across unrelated tests

```python
# Good
def test_process_method(process_method_factory):
    pm = process_method_factory.create(name="Test Method")
    assert pm.name == "Test Method"

# Bad
def test_process_method():
    pm = ProcessMethod(
        name="Test Method",
        description="Long description...",
        file_name="file.txt",
        # ... many more fields
    )
```

### 3. Assertion Clarity

**Do**:
- Use specific assertions
- Include helpful error messages
- Test one concept per test

**Don't**:
- Use generic `assert True`
- Test multiple unrelated things in one test

```python
# Good
def test_process_method_name_required():
    with pytest.raises(ValueError, match="name is required"):
        ProcessMethod(name=None)

# Bad
def test_process_method():
    pm = ProcessMethod(name="Test")
    assert pm.name  # What specifically are we testing?
    assert pm.id   # Different concept
    assert len(pm.parts) == 0  # Another concept
```

### 4. Mock Usage

**Do**:
- Mock external dependencies
- Mock at the boundary
- Use mocks for unit tests

**Don't**:
- Mock the system under test
- Over-mock in integration tests

```python
# Good - Unit test with mocks
@patch('process_navigator.utils.file_handling.open')
def test_file_upload(mock_open):
    mock_open.return_value.__enter__.return_value.read.return_value = b"data"
    result = process_file_upload("file.txt")
    assert result == "data"

# Good - Integration test without mocks
def test_file_upload_integration(client, temp_file_storage):
    data = {"file": (io.BytesIO(b"data"), "file.txt")}
    response = client.post("/upload", data=data)
    assert response.status_code == 200
```

### 5. Performance

**Do**:
- Use appropriate data volumes
- Mark slow tests
- Use session-scoped fixtures for expensive setup

**Don't**:
- Load large datasets for simple tests
- Recreate database for every test unnecessarily

```python
# Good
@pytest.fixture(scope="session")
def expensive_computation():
    return compute_large_dataset()

@pytest.mark.slow
def test_large_dataset(expensive_computation):
    assert len(expensive_computation) > 1000

# Bad
def test_simple_query():
    # Loads thousands of records for testing a simple query
    load_large_dataset()
    result = query_single_record()
```

### 6. Test Documentation

**Do**:
- Write clear docstrings
- Document complex test scenarios
- Explain why, not just what

```python
def test_process_path_expansion_with_duplicate_inputs():
    """
    Test that path expansion correctly handles duplicate inputs.
    
    When a user selects the same input multiple times in different steps,
    the expansion should create separate paths for each occurrence.
    This is a regression test for bug #123.
    """
```

### 7. Error Testing

**Do**:
- Test error conditions
- Test edge cases
- Test validation logic

```python
def test_email_validation_rejects_invalid_format():
    form = RegistrationForm(email="not-an-email")
    assert not form.validate()
    assert "email" in form.errors

def test_division_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

---

## Getting Started

### Setting Up the New Structure

1. **Create Directory Structure**
   ```bash
   mkdir -p tests/{unit,integration,system,performance,data/scenarios,utils,fixtures}
   touch tests/{unit,integration,system,performance,utils,fixtures}/__init__.py
   ```

2. **Create Configuration File**
   ```bash
   cat > tests/pytest.ini << EOF
   [pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   markers =
       unit: Unit tests
       integration: Integration tests
       system: System tests
       performance: Performance tests
       smoke: Smoke tests
       slow: Slow tests
       database: Database tests
       critical: Critical functionality
   EOF
   ```

3. **Migrate Existing Tests**
   - Move route tests to `integration/`
   - Extract model logic tests to `unit/`
   - Create system tests from existing user path tests

4. **Create Utility Modules**
   - `utils/assertions.py`
   - `utils/factories.py`
   - `utils/generators.py`
   - `utils/helpers.py`

5. **Enhance Test Data**
   - Add scenarios to `data/scenarios/`
   - Create JSON schemas
   - Add parametrization data

### Writing Your First Tests

#### Unit Test Example

```python
# tests/unit/test_models_process.py
import pytest
from process_navigator.models.process import ProcessMethod, ProcessMethodPart

@pytest.mark.unit
def test_process_method_creation_with_valid_data():
    """Test ProcessMethod can be created with valid data"""
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    assert pm.name == "Test Method"
    assert pm.description == "Test Description"
    assert pm.file_name == "test.txt"

@pytest.mark.unit
def test_process_method_parts_relationship():
    """Test ProcessMethod to ProcessMethodPart relationship"""
    pm = ProcessMethod(name="Test", description="Desc", file_name="file.txt")
    part = ProcessMethodPart(name="Part 1", process_method=pm)
    
    assert len(pm.process_method_parts) == 1
    assert pm.process_method_parts[0] == part
    assert part.process_method == pm
```

#### Integration Test Example

```python
# tests/integration/test_data_routes.py
import pytest
from process_navigator.models.process import ProcessMethod

@pytest.mark.integration
@pytest.mark.database
def test_create_process_method_persists_to_database(client, test_app, route_options):
    """Test creating a process method persists to database"""
    # Register and login
    client.post("/register", data={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password",
        "submit": True
    })
    client.post("/login", data={
        "email": "test@example.com",
        "password": "password",
        "submit": True
    })
    
    # Create process method
    response = client.post("/data/add_process_method", data={
        "name": "New Method",
        "description": "New Description",
        "submit": True
    })
    
    # Verify database persistence
    with test_app.app_context():
        pm = db.session.query(ProcessMethod).filter_by(name="New Method").first()
        assert pm is not None
        assert pm.description == "New Description"
```

#### System Test Example

```python
# tests/system/test_user_journeys.py
import pytest

@pytest.mark.system
@pytest.mark.slow
def test_complete_process_creation_workflow(client, route_options):
    """Test user can complete full process creation workflow"""
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
        "process_method_post_add_method",
        "add_process_method_get"
    ]
    
    response = provide_stacked_response(client, paths, route_options)
    
    assert response.status_code == 200
    assert b"Add Process Method" in response.data
```

---

## Future Enhancements

### Phase 1: Foundation (Months 1-2)

- [ ] Implement new directory structure
- [ ] Migrate existing tests to new structure
- [ ] Create core utility modules
- [ ] Enhance test data with scenarios
- [ ] Add JSON schemas for all data files
- [ ] Create factories for all models
- [ ] Achieve 60% code coverage

### Phase 2: Expansion (Months 3-4)

- [ ] Add comprehensive unit tests for all models
- [ ] Create integration tests for all routes
- [ ] Develop system tests for all user journeys
- [ ] Add performance testing framework
- [ ] Implement parallel test execution
- [ ] Achieve 70% code coverage

### Phase 3: Advanced Features (Months 5-6)

- [ ] Add UI testing with Selenium/Playwright
- [ ] Implement API testing framework (when API exists)
- [ ] Create load testing scenarios
- [ ] Add security testing
- [ ] Implement mutation testing
- [ ] Achieve 80%+ code coverage

### Phase 4: Automation (Months 7+)

- [ ] Set up CI/CD pipeline with automated testing
- [ ] Implement pre-commit hooks with tests
- [ ] Add automated performance regression detection
- [ ] Create test report dashboard
- [ ] Implement automatic test generation from schemas
- [ ] Add visual regression testing

### Advanced Testing Techniques

#### Contract Testing
For when APIs are added:
```python
@pytest.mark.contract
def test_api_contract_get_process_methods():
    """Test API contract for GET /api/process_methods"""
    response = client.get("/api/process_methods")
    schema = load_schema("process_methods_response.json")
    validate_contract(response.json(), schema)
```

#### Property-Based Testing
Using hypothesis:
```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=100))
def test_process_method_name_accepts_any_valid_string(name):
    pm = ProcessMethod(name=name, description="Test", file_name="test.txt")
    assert pm.name == name
```

#### Mutation Testing
Using mutmut to find weak tests:
```bash
mutmut run
mutmut results
```

#### Visual Regression Testing
Using pytest-visual:
```python
def test_home_page_appearance(browser, visual_regression):
    browser.get("/")
    visual_regression.capture_screenshot("home_page")
```

---

## Appendix

### A. JSON Schema Templates

#### Route Options Schema
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "route": {"type": "string"},
    "method": {"type": "string", "enum": ["GET", "POST"]},
    "data": {"type": "object"},
    "expected_status": {"type": "integer"},
    "expected_redirect": {"type": "string"},
    "tags": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["name", "route", "method", "data"]
}
```

#### Test Data Schema
```json
{
  "type": "object",
  "properties": {
    "ProcessMethods": {"type": "array"},
    "BaseUnits": {"type": "array"},
    "scenarios": {"type": "object"}
  }
}
```

### B. Useful Commands

```bash
# Run tests with coverage report
pytest --cov=process_navigator --cov-report=html --cov-report=term

# Run only failed tests from last run
pytest --lf

# Run tests that match a keyword
pytest -k "process_method"

# Show slowest tests
pytest --durations=10

# Generate test report
pytest --html=report.html --self-contained-html

# Run tests in random order (requires pytest-random-order)
pytest --random-order

# Profile test execution
pytest --profile

# Debug mode (drop into pdb on failure)
pytest --pdb
```

### C. References

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Flask Applications](https://flask.palletsprojects.com/en/latest/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [Test-Driven Development by Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)

### D. Migration Checklist

- [ ] Create new directory structure
- [ ] Set up pytest.ini with markers
- [ ] Create fixture modules in `fixtures/`
- [ ] Create utility modules in `utils/`
- [ ] Migrate `test_home_routes.py` → `integration/test_home_routes.py`
- [ ] Migrate `test_data_routes.py` → `integration/test_data_routes.py`
- [ ] Migrate `test_cauldron_routes.py` → `integration/test_cauldron_routes.py`
- [ ] Extract unit tests from route tests → `unit/test_models_*.py`
- [ ] Create system tests from user paths → `system/test_user_journeys.py`
- [ ] Enhance `route_options.json` with new fields
- [ ] Create scenario files in `data/scenarios/`
- [ ] Add JSON schemas for all data files
- [ ] Update CI/CD configuration (if exists)
- [ ] Update documentation
- [ ] Train team on new structure

---

## Conclusion

This testing framework provides a solid foundation for comprehensive testing throughout the project's lifetime. By following the data-driven approach and clear separation of test levels, the framework enables:

1. **Rapid test creation**: Add new test cases by editing JSON files
2. **Easy maintenance**: Clear organization and reusable components
3. **Comprehensive coverage**: Unit, integration, system, and performance tests
4. **Scalability**: Structure supports growth from current state to enterprise-scale
5. **Quality assurance**: Catches bugs at every level of the application

The framework is designed to evolve with the project, starting with the essentials and growing to include advanced testing techniques as needed.
