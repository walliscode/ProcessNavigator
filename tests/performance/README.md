# Performance Tests

This directory contains performance tests for ProcessNavigator.

## Purpose

Performance tests verify that the application meets performance requirements:
- Response time under load
- Query performance with large datasets
- Scalability limits
- Resource usage

## What to Test

- Page load times with various data volumes
- Database query performance
- Process path expansion with many combinations
- Concurrent user operations
- File upload/download performance
- Search and filtering performance

## Organization

Tests are organized by performance aspect:
- `test_query_performance.py`: Database query performance
- `test_load_handling.py`: Application load and scalability
- `test_path_expansion.py`: Process path expansion performance

## Running Performance Tests

```bash
# Run all performance tests
pytest tests/performance/ -v

# Run specific test file
pytest tests/performance/test_query_performance.py

# Run with marker
pytest -m performance

# Note: Performance tests are typically slow
```

## Example Test

```python
import pytest
import time
from tests.utils.generators import generate_test_scenario
from tests.utils.assertions import assert_database_count

@pytest.mark.performance
@pytest.mark.slow
def test_query_performance_with_large_dataset(test_app):
    """Test query performance with 1000 process methods"""
    from process_navigator.extensions.database import db
    from process_navigator.models.process import ProcessMethod
    
    # Setup: create large dataset
    with test_app.app_context():
        scenario = generate_test_scenario("large")
        # Load scenario data into database
        # ... (data loading logic)
        
        # Measure query time
        start_time = time.time()
        results = db.session.query(ProcessMethod).all()
        query_time = time.time() - start_time
        
        # Assert: query should complete in reasonable time
        assert len(results) == 1000
        assert query_time < 1.0, f"Query took {query_time:.2f}s, expected <1.0s"

@pytest.mark.performance
def test_process_path_expansion_performance(client, test_app):
    """Test path expansion with 1000 combinations"""
    # Test that path expansion with many inputs/parameters
    # completes in reasonable time
    start_time = time.time()
    
    # Trigger path expansion
    # ... (expansion logic)
    
    expansion_time = time.time() - start_time
    assert expansion_time < 5.0, f"Expansion took {expansion_time:.2f}s"
```

## Best Practices

1. **Set Baselines**: Establish performance baselines early
2. **Use Large Datasets**: Test with realistic data volumes
3. **Measure Accurately**: Use precise timing
4. **Document Requirements**: Clearly state performance expectations
5. **Monitor Trends**: Track performance over time
6. **Isolate Tests**: Run performance tests separately from unit/integration
7. **Clean Up**: Ensure large datasets are cleaned up after tests

## Performance Targets

Based on PROJECT_PLAN.md, target metrics are:
- Page load time: <2 seconds
- API response time: <500ms (95th percentile)
- Database query time: <100ms (average)
- Support 100+ concurrent users
