# Testing Framework Quick Reference

## 🚀 Quick Start

```bash
# Run all tests
pytest

# Run specific level
pytest tests/unit/          # Fast unit tests
pytest tests/integration/   # Integration tests  
pytest tests/system/        # End-to-end tests

# Run by marker
pytest -m unit              # Only unit tests
pytest -m "not slow"        # Skip slow tests
pytest -m critical          # Critical tests only

# With coverage
pytest --cov=process_navigator --cov-report=html
```

## 📁 Directory Structure

```
tests/
├── unit/              Unit tests (fast, no database)
├── integration/       Integration tests (with database)
├── system/           System tests (end-to-end)
├── performance/      Performance tests
├── utils/            Reusable utilities
│   ├── assertions.py  Custom assertions
│   ├── helpers.py     Helper functions
│   ├── factories.py   Data factories
│   └── generators.py  Data generators
├── data/
│   ├── scenarios/     Test scenarios
│   ├── route_options.json
│   └── test_data.json
└── conftest.py       Global fixtures
```

## 🧪 Test Levels

| Level | Purpose | Database | Speed | Volume |
|-------|---------|----------|-------|--------|
| **Unit** | Test functions/classes in isolation | ❌ No | <100ms | 70-80% |
| **Integration** | Test components together | ✅ Yes | 1-5s | 15-25% |
| **System** | Test complete workflows | ✅ Yes | 5-30s | 5-10% |
| **Performance** | Test performance requirements | ✅ Yes | Varies | As needed |

## 🏷️ Test Markers

```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.system        # System test
@pytest.mark.performance   # Performance test
@pytest.mark.slow          # Slow test (>5s)
@pytest.mark.critical      # Critical functionality
@pytest.mark.database      # Requires database
@pytest.mark.authentication # Auth-related
```

## 📝 Writing Tests

### Unit Test Template

```python
import pytest

@pytest.mark.unit
def test_model_creation():
    """Test Model can be instantiated."""
    from process_navigator.models import Model
    
    instance = Model(name="Test")
    assert instance.name == "Test"
```

### Integration Test Template

```python
import pytest
from tests.utils.helpers import register_and_login
from tests.utils.assertions import assert_database_has_record

@pytest.mark.integration
@pytest.mark.database
def test_route_handler(client, test_app):
    """Test route handler persists data."""
    register_and_login(client)
    
    response = client.post("/endpoint", data={"name": "Test"})
    
    with test_app.app_context():
        from process_navigator.extensions.database import db
        from process_navigator.models import Model
        assert_database_has_record(Model, db.session, name="Test")
```

### System Test Template

```python
import pytest
from tests.utils.helpers import provide_stacked_response
from tests.utils.assertions import assert_status_code

@pytest.mark.system
@pytest.mark.slow
def test_complete_workflow(client, route_options):
    """Test complete user workflow."""
    paths = ["register_user", "login_user", "endpoint_get"]
    response = provide_stacked_response(client, paths, route_options)
    assert_status_code(response, 200)
```

## 🛠️ Utilities Cheat Sheet

### Common Assertions

```python
from tests.utils.assertions import *

# Response assertions
assert_status_code(response, 200)
assert_response_contains(response, "Welcome")
assert_redirects_to(response, "/login")

# Database assertions
assert_database_count(Model, 5, db_session)
assert_database_has_record(Model, db_session, name="Test")
assert_database_empty(Model, db_session)

# Session assertions
assert_session_keys(client, ["user_id", "token"])
assert_session_key_value(client, "user_id", 123)
```

### Common Helpers

```python
from tests.utils.helpers import *

# User operations
login_user(client, email="test@example.com", password="pass")
register_and_login(client, email="test@example.com")

# Data loading
data = load_json_data("route_options.json")
scenario = load_test_scenario("edge_cases.json")

# Request sequences
response = provide_stacked_response(client, paths, route_options)

# Session operations
set_session_value(client, "key", "value")
value = get_session_value(client, "key")
```

### Using Factories

```python
from tests.utils.factories import *

# Create single instance
pm = ProcessMethodFactory.create(db_session, name="Custom Name")

# Create multiple instances
pms = ProcessMethodFactory.create_batch(db_session, 5)

# Create without persisting
data = ProcessMethodFactory.build(name="Test")

# Create complete scenario
scenario = create_complete_test_scenario(db_session)
# Returns dict with all entities
```

### Using Generators

```python
from tests.utils.generators import *

# Generate test data
methods = generate_process_methods(count=10, with_parts=True)
inputs = generate_inputs(count=50)

# Generate scenarios
scenario = generate_test_scenario("minimal")  # or "standard", "large"

# Generate edge cases
edge_cases = generate_edge_case_data()
```

## 📊 Test Data Files

### route_options.json
Defines HTTP requests:
```json
{
  "name": "login_user",
  "route": "/login",
  "method": "POST",
  "data": {"email": "test@example.com", "password": "pass"}
}
```

### test_data.json
Database seed data:
```json
{
  "ProcessMethods": [...],
  "Inputs": [...],
  "Parameters": [...]
}
```

### scenarios/edge_cases.json
Edge case test data:
```json
{
  "empty_values": {...},
  "special_characters": {...},
  "boundary_values": {...}
}
```

## 🎯 Common Tasks

### Add New Test

1. Choose appropriate directory (unit/integration/system)
2. Create test file: `test_<feature>.py`
3. Add markers: `@pytest.mark.unit`
4. Use utilities for assertions and helpers
5. Follow naming: `test_<component>_<action>_<expected>`

### Add Test Data

1. **For database seeds**: Edit `tests/data/test_data.json`
2. **For HTTP requests**: Edit `tests/data/route_options.json`
3. **For scenarios**: Create file in `tests/data/scenarios/`
4. **Validate**: Ensure schema compliance

### Run Specific Tests

```bash
# By file
pytest tests/unit/test_models_process.py

# By test name
pytest tests/unit/test_models_process.py::test_creation

# By keyword
pytest -k "process_method"

# By multiple markers
pytest -m "integration and database"
```

### Debug Tests

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Drop into debugger
pytest --pdb

# Show local variables
pytest -l
```

## 📚 Documentation

| Document | Purpose | Location |
|----------|---------|----------|
| **TESTING_FRAMEWORK.md** | Complete framework docs | Root |
| **tests/README.md** | Testing suite overview | tests/ |
| **MIGRATION_GUIDE.md** | Migration instructions | tests/ |
| **TESTING_SUMMARY.md** | Implementation summary | Root |
| **Directory READMEs** | Level-specific guides | tests/{unit,integration,system}/ |

## 🎨 Example Tests

See example test files:
- `tests/unit/test_models_process_example.py` - Unit test examples
- `tests/integration/test_example_integration.py` - Integration examples
- `tests/system/test_example_system.py` - System test examples

## 💡 Best Practices

1. ✅ **Write independent tests** - No dependencies between tests
2. ✅ **Use descriptive names** - Clear test purpose
3. ✅ **Keep unit tests fast** - <100ms execution
4. ✅ **Use appropriate level** - Unit for logic, integration for database
5. ✅ **Leverage utilities** - Don't reinvent the wheel
6. ✅ **Add markers** - Enable filtering
7. ✅ **Document complex scenarios** - Explain "why"
8. ✅ **Clean up after tests** - Use fixtures

## 🔧 Troubleshooting

### Tests Not Found
```bash
# Check pytest can discover tests
pytest --collect-only

# Ensure __init__.py exists in test directories
```

### Import Errors
```bash
# Check PYTHONPATH includes project root
export PYTHONPATH=/path/to/ProcessNavigator:$PYTHONPATH

# Or run from project root
cd /path/to/ProcessNavigator && pytest
```

### Database Issues
```python
# Ensure test_app fixture is used
def test_something(test_app):
    with test_app.app_context():
        # database operations
```

### Fixture Not Found
```bash
# Check conftest.py is in correct location
# Ensure fixture is defined in conftest.py or imported
```

## 📈 Coverage

```bash
# Generate coverage report
pytest --cov=process_navigator --cov-report=html --cov-report=term

# View HTML report
# open htmlcov/index.html

# Show missing lines
pytest --cov=process_navigator --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=process_navigator --cov-fail-under=80
```

## 🚦 CI/CD Integration (Future)

```yaml
# Example .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## 📞 Getting Help

1. Start with `tests/README.md`
2. Check `TESTING_FRAMEWORK.md` for details
3. Review example tests
4. Consult directory READMEs
5. Ask in team meetings

## 🎯 Quick Commands

```bash
# Fast development cycle (unit tests only)
pytest tests/unit/ -v

# Pre-commit checks (exclude slow tests)
pytest -m "not slow" --cov=process_navigator

# Full validation
pytest --cov=process_navigator --cov-report=html

# Debug specific test
pytest tests/unit/test_models.py::test_creation -vv --pdb
```

---

**For complete documentation, see [TESTING_FRAMEWORK.md](../TESTING_FRAMEWORK.md)**
