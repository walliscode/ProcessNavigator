# Test Scenarios

This directory contains scenario-specific test data files.

## Purpose

Scenario files provide test data for specific testing situations:
- Edge cases and boundary values
- Performance testing with large datasets
- Complex workflows
- Error conditions

## Available Scenarios

### minimal_scenario.json
Minimal test data for fast unit tests. Contains only the essential data needed to test basic functionality.

**Use for:**
- Quick unit tests
- Testing basic model creation
- Rapid iteration during development

### edge_cases.json
Comprehensive edge case data for validation testing.

**Includes:**
- Empty values
- Long values (testing field length limits)
- Special characters (XSS, SQL injection attempts)
- Unicode and internationalization
- Null values
- Duplicate values
- Invalid references
- Invalid formats
- Boundary values

**Use for:**
- Validation testing
- Security testing
- Boundary testing
- Error handling verification

### large_dataset.json (Future)
Large dataset for performance testing.

**Will include:**
- 1000+ process methods
- 10,000+ inputs
- Complex relationships

**Use for:**
- Performance testing
- Load testing
- Query optimization verification

## Using Scenarios in Tests

### Loading Scenario Data

```python
from tests.utils.helpers import load_test_scenario

# Load scenario
scenario = load_test_scenario("edge_cases.json")

# Access specific data
empty_values = scenario["empty_values"]
special_chars = scenario["special_characters"]
```

### Parametrized Tests with Scenarios

```python
import pytest
from tests.utils.helpers import load_test_scenario

scenario = load_test_scenario("edge_cases.json")

@pytest.mark.parametrize(
    "cas_number",
    scenario["invalid_formats"]["cas_numbers"]
)
def test_invalid_cas_format(cas_number):
    # Test that invalid CAS numbers are rejected
    with pytest.raises(ValidationError):
        validate_cas_number(cas_number)
```

### Integration Test with Scenario

```python
def test_xss_prevention(client, test_app):
    """Test that XSS attempts are properly escaped"""
    scenario = load_test_scenario("edge_cases.json")
    xss_data = scenario["special_characters"]["xss_attempt"]
    
    response = client.post("/data/add_process_method", data=xss_data)
    
    # Verify XSS is escaped in response
    assert "<script>" not in response.data.decode()
    assert "&lt;script&gt;" in response.data.decode()
```

## Creating New Scenarios

When creating new scenario files:

1. Use descriptive file names (e.g., `complex_workflows.json`)
2. Add a `description` field at the top
3. Organize data logically into sections
4. Document the purpose of each section
5. Update this README with the new scenario

### Scenario Template

```json
{
  "description": "Purpose of this scenario",
  "section_name": {
    "test_case_1": {
      "name": "value",
      "other_field": "value"
    },
    "test_case_2": {
      "name": "value",
      "other_field": "value"
    }
  },
  "another_section": {
    "data": []
  }
}
```

## Best Practices

1. **Keep Scenarios Focused**: Each scenario should have a clear purpose
2. **Document Intent**: Add descriptions and comments
3. **Realistic Data**: Use realistic values when possible
4. **Comprehensive Coverage**: Include all relevant edge cases
5. **Maintainability**: Organize data logically
6. **Reusability**: Design for reuse across multiple tests

## Scenario Organization

```
scenarios/
├── README.md (this file)
├── minimal_scenario.json        # Minimal data for fast tests
├── edge_cases.json              # Edge cases and validation
├── complex_workflows.json       # Complex multi-step workflows
├── large_dataset.json           # Large data for performance tests
└── error_scenarios.json         # Error conditions
```

## Future Enhancements

- [ ] Create `large_dataset.json` for performance testing
- [ ] Create `complex_workflows.json` for multi-step processes
- [ ] Create `error_scenarios.json` for error handling
- [ ] Add JSON schemas for scenario validation
- [ ] Create scenario generator scripts
- [ ] Add realistic chemical data scenarios
