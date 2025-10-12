# Testing Framework Migration Guide

This guide helps migrate the existing test suite to the new comprehensive testing framework.

## Overview

The new testing framework introduces:
- Clear separation of test levels (unit, integration, system, performance)
- Reusable utilities (assertions, factories, generators, helpers)
- Enhanced data-driven testing capabilities
- Better organization and maintainability

## Migration Steps

### Phase 1: Setup New Structure (Immediate)

1. **Verify Directory Structure**
   ```bash
   # The following directories should exist:
   tests/
   ├── unit/
   ├── integration/
   ├── system/
   ├── performance/
   ├── utils/
   ├── fixtures/
   └── data/scenarios/
   ```

2. **Review pytest.ini**
   - Check that markers are properly configured
   - Adjust test discovery patterns if needed
   - Review logging configuration

3. **Test Utilities**
   - Review `tests/utils/assertions.py` for custom assertions
   - Review `tests/utils/helpers.py` for helper functions
   - Review `tests/utils/factories.py` for data factories
   - Review `tests/utils/generators.py` for data generators

### Phase 2: Migrate Existing Tests (1-2 weeks)

#### Step 1: Move Integration Tests

Current integration tests are in the root `tests/` directory. Move them to `tests/integration/`:

```bash
# Move existing route tests
mv tests/test_home_routes.py tests/integration/
mv tests/test_data_routes.py tests/integration/
mv tests/test_cauldron_routes.py tests/integration/
mv tests/test_data.py tests/integration/test_database_relationships.py
```

#### Step 2: Update Test Imports

In each moved test file, update imports to use the new utilities:

**Before:**
```python
from tests.utils import provide_stacked_response
```

**After:**
```python
from tests.utils.helpers import provide_stacked_response
from tests.utils.assertions import assert_response_contains, assert_status_code
```

#### Step 3: Add Test Markers

Add appropriate markers to each test:

```python
import pytest

@pytest.mark.integration
@pytest.mark.database
def test_login_route(client, route_options):
    # test code
```

#### Step 4: Refactor Using New Utilities

Replace manual assertions with utility functions:

**Before:**
```python
assert response.status_code == 200
assert b"Welcome" in response.data
```

**After:**
```python
from tests.utils.assertions import assert_status_code, assert_response_contains

assert_status_code(response, 200)
assert_response_contains(response, "Welcome")
```

### Phase 3: Extract Unit Tests (2-3 weeks)

Extract model and utility tests from integration tests into unit tests:

#### Example: Extract Model Tests

**From `tests/integration/test_database_relationships.py`:**

Create `tests/unit/test_models_process.py`:

```python
import pytest
from process_navigator.models.process import ProcessMethod, ProcessMethodPart

@pytest.mark.unit
def test_process_method_creation():
    """Test ProcessMethod instantiation"""
    pm = ProcessMethod(
        name="Test Method",
        description="Test Description",
        file_name="test.txt"
    )
    assert pm.name == "Test Method"
    assert pm.description == "Test Description"
    assert pm.file_name == "test.txt"

@pytest.mark.unit
def test_process_method_part_relationship():
    """Test ProcessMethod to ProcessMethodPart relationship"""
    pm = ProcessMethod(name="Test", description="Desc", file_name="file.txt")
    part = ProcessMethodPart(name="Part 1", process_method=pm)
    
    assert len(pm.process_method_parts) == 1
    assert pm.process_method_parts[0] == part
    assert part.process_method == pm
```

#### Create Unit Tests for Each Model

Create separate test files for each model module:
- `tests/unit/test_models_process.py`
- `tests/unit/test_models_units.py`
- `tests/unit/test_models_inputs.py`
- `tests/unit/test_models_parameters.py`
- `tests/unit/test_models_analysis.py`
- `tests/unit/test_models_admin.py`

### Phase 4: Create System Tests (1-2 weeks)

Create end-to-end workflow tests in `tests/system/`:

#### Example: User Journey Test

Create `tests/system/test_user_journeys.py`:

```python
import pytest
from tests.utils.helpers import provide_stacked_response

@pytest.mark.system
@pytest.mark.slow
def test_complete_process_creation_journey(client, route_options):
    """Test complete user journey from registration to process creation"""
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

### Phase 5: Enhance Test Data (Ongoing)

#### Add Scenario Files

Create scenario-specific data files in `tests/data/scenarios/`:

**`tests/data/scenarios/edge_cases.json`:**
```json
{
  "empty_strings": {
    "process_method": {
      "name": "",
      "description": "Test with empty name"
    }
  },
  "long_strings": {
    "process_method": {
      "name": "A very long name that exceeds normal expectations...",
      "description": "Normal description"
    }
  }
}
```

#### Enhance route_options.json

Add new fields to route options for better validation:

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

## Testing the Migration

### Run Tests by Level

```bash
# Run only unit tests (should be fast)
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run only system tests
pytest tests/system/ -v

# Run all tests
pytest
```

### Run Tests by Marker

```bash
# Run only database tests
pytest -m database

# Run critical tests only
pytest -m critical

# Run fast tests (exclude slow)
pytest -m "not slow"
```

### Check Coverage

```bash
# Run with coverage report
pytest --cov=process_navigator --cov-report=html --cov-report=term

# View HTML report
# open htmlcov/index.html
```

## Common Migration Issues

### Issue 1: Import Errors

**Problem:** `ModuleNotFoundError: No module named 'tests.utils'`

**Solution:** Ensure `tests/utils/__init__.py` exists and is not empty.

### Issue 2: Fixture Not Found

**Problem:** `fixture 'route_options' not found`

**Solution:** Check that `conftest.py` is in the right location and fixtures are properly defined.

### Issue 3: Database Pollution

**Problem:** Tests fail due to leftover data from previous tests

**Solution:** Ensure proper cleanup in fixtures:

```python
@pytest.fixture
def test_app():
    app = create_app(test_config=True)
    with app.app_context():
        db.drop_all()
        db.create_all()
        # load test data
    
    yield app
    
    with app.app_context():
        db.drop_all()  # Clean up after tests
```

### Issue 4: Test Order Dependencies

**Problem:** Tests pass individually but fail when run together

**Solution:** Make tests independent. Each test should set up its own data and not rely on other tests.

## Checklist

Use this checklist to track your migration progress:

### Setup
- [ ] Verify directory structure is created
- [ ] Review and configure pytest.ini
- [ ] Test utilities are accessible
- [ ] Review TESTING_FRAMEWORK.md

### Integration Tests
- [ ] Move test_home_routes.py to integration/
- [ ] Move test_data_routes.py to integration/
- [ ] Move test_cauldron_routes.py to integration/
- [ ] Move test_data.py to integration/ (rename to test_database_relationships.py)
- [ ] Update imports in migrated tests
- [ ] Add @pytest.mark.integration markers
- [ ] Refactor using new assertion helpers
- [ ] Verify all integration tests pass

### Unit Tests
- [ ] Create tests/unit/test_models_process.py
- [ ] Create tests/unit/test_models_units.py
- [ ] Create tests/unit/test_models_inputs.py
- [ ] Create tests/unit/test_models_parameters.py
- [ ] Create tests/unit/test_models_analysis.py
- [ ] Create tests/unit/test_models_admin.py
- [ ] Create tests/unit/test_cauldron_models.py
- [ ] Create tests/unit/test_utils.py
- [ ] Create tests/unit/test_decorators.py
- [ ] Add @pytest.mark.unit markers
- [ ] Verify all unit tests pass

### System Tests
- [ ] Create tests/system/test_user_journeys.py
- [ ] Create tests/system/test_process_workflows.py
- [ ] Create tests/system/test_error_scenarios.py
- [ ] Add @pytest.mark.system markers
- [ ] Add @pytest.mark.slow markers where appropriate
- [ ] Verify all system tests pass

### Test Data
- [ ] Create scenario files in data/scenarios/
- [ ] Enhance route_options.json with new fields
- [ ] Create JSON schemas for new data files
- [ ] Add validation in conftest.py

### Utilities
- [ ] Review and customize assertions.py
- [ ] Review and customize helpers.py
- [ ] Create factories for all models
- [ ] Create generators for test scenarios

### Validation
- [ ] All tests pass: `pytest`
- [ ] Tests can run in parallel: `pytest -n auto`
- [ ] Coverage is maintained or improved
- [ ] Fast tests run quickly (<1s per test)
- [ ] Documentation is updated

## Next Steps

After completing the migration:

1. **Add New Tests**: Use the framework to add new tests for uncovered code
2. **Performance Tests**: Create performance tests in `tests/performance/`
3. **Continuous Improvement**: Regularly review and refactor tests
4. **Documentation**: Keep test documentation up to date
5. **Team Training**: Train team members on the new framework

## Getting Help

- Review `TESTING_FRAMEWORK.md` for comprehensive documentation
- Check existing tests in the new structure for examples
- Review pytest documentation: https://docs.pytest.org/
- Ask questions in team meetings or code reviews

## Timeline

Suggested timeline for migration:

- **Week 1**: Setup structure, move integration tests
- **Week 2**: Extract unit tests from integration tests
- **Week 3**: Create system tests, enhance test data
- **Week 4**: Final validation, documentation, team training

Adjust timeline based on team size and project priorities.
