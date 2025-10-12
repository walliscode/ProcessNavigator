"""
Custom assertion helpers for tests.

These helpers make tests more readable and provide better error messages.
"""


def assert_response_contains(response, expected_content, encoding="utf-8"):
    """
    Assert that response contains expected content.
    
    Args:
        response: Flask test response object
        expected_content: String or list of strings to find in response
        encoding: Character encoding (default: utf-8)
    
    Raises:
        AssertionError: If content is not found
    """
    if isinstance(expected_content, str):
        expected_content = [expected_content]
    
    response_data = response.data.decode(encoding) if isinstance(response.data, bytes) else response.data
    
    for content in expected_content:
        assert content in response_data, (
            f"Expected content '{content}' not found in response. "
            f"Response preview: {response_data[:500]}"
        )


def assert_response_not_contains(response, unexpected_content, encoding="utf-8"):
    """
    Assert that response does not contain unexpected content.
    
    Args:
        response: Flask test response object
        unexpected_content: String or list of strings that should not be in response
        encoding: Character encoding (default: utf-8)
    """
    if isinstance(unexpected_content, str):
        unexpected_content = [unexpected_content]
    
    response_data = response.data.decode(encoding) if isinstance(response.data, bytes) else response.data
    
    for content in unexpected_content:
        assert content not in response_data, (
            f"Unexpected content '{content}' found in response."
        )


def assert_database_count(model, expected_count, db_session):
    """
    Assert that database has expected record count for a model.
    
    Args:
        model: SQLAlchemy model class
        expected_count: Expected number of records
        db_session: Database session
    
    Raises:
        AssertionError: If count doesn't match
    """
    from sqlalchemy import select
    
    actual_count = db_session.execute(select(model)).scalars().all()
    actual_count = len(actual_count)
    
    assert actual_count == expected_count, (
        f"Expected {expected_count} {model.__name__} records, "
        f"but found {actual_count}"
    )


def assert_database_has_record(model, db_session, **filters):
    """
    Assert that database has a record matching the filters.
    
    Args:
        model: SQLAlchemy model class
        db_session: Database session
        **filters: Keyword arguments for filtering (e.g., name="Test")
    
    Raises:
        AssertionError: If no matching record found
    """
    from sqlalchemy import select
    
    query = select(model)
    for key, value in filters.items():
        query = query.filter(getattr(model, key) == value)
    
    result = db_session.execute(query).scalar()
    
    assert result is not None, (
        f"No {model.__name__} record found with filters: {filters}"
    )
    
    return result


def assert_database_empty(model, db_session):
    """
    Assert that database has no records for a model.
    
    Args:
        model: SQLAlchemy model class
        db_session: Database session
    """
    assert_database_count(model, 0, db_session)


def assert_session_keys(client, expected_keys):
    """
    Assert that session has expected keys.
    
    Args:
        client: Flask test client
        expected_keys: List of keys that should exist in session
    
    Raises:
        AssertionError: If keys are missing
    """
    with client.session_transaction() as session:
        missing_keys = [key for key in expected_keys if key not in session]
        assert not missing_keys, (
            f"Session is missing keys: {missing_keys}. "
            f"Available keys: {list(session.keys())}"
        )


def assert_session_key_value(client, key, expected_value):
    """
    Assert that session key has expected value.
    
    Args:
        client: Flask test client
        key: Session key
        expected_value: Expected value for the key
    """
    with client.session_transaction() as session:
        assert key in session, f"Session key '{key}' not found"
        assert session[key] == expected_value, (
            f"Session key '{key}' has value '{session[key]}', "
            f"expected '{expected_value}'"
        )


def assert_redirects_to(response, expected_location):
    """
    Assert that response redirects to expected location.
    
    Args:
        response: Flask test response object
        expected_location: Expected redirect location (URL path)
    """
    assert response.status_code in (301, 302, 303, 307, 308), (
        f"Expected redirect status code (3xx), got {response.status_code}"
    )
    
    actual_location = response.headers.get("Location", "")
    assert expected_location in actual_location, (
        f"Expected redirect to '{expected_location}', "
        f"but got '{actual_location}'"
    )


def assert_flash_message(response, expected_message, category=None):
    """
    Assert that flash message is present in response.
    
    Args:
        response: Flask test response object
        expected_message: Expected flash message text
        category: Optional flash message category (e.g., 'success', 'error')
    
    Note: This checks the response HTML for the message.
    For more robust testing, you may need to check session['_flashes']
    """
    response_data = response.data.decode("utf-8") if isinstance(response.data, bytes) else response.data
    
    assert expected_message in response_data, (
        f"Flash message '{expected_message}' not found in response"
    )


def assert_status_code(response, expected_status):
    """
    Assert response status code with helpful error message.
    
    Args:
        response: Flask test response object
        expected_status: Expected HTTP status code
    """
    assert response.status_code == expected_status, (
        f"Expected status code {expected_status}, got {response.status_code}. "
        f"Response: {response.data[:200]}"
    )


def assert_json_structure(response, expected_keys):
    """
    Assert that JSON response has expected keys.
    
    Args:
        response: Flask test response object
        expected_keys: List of keys expected in JSON response
    """
    json_data = response.get_json()
    assert json_data is not None, "Response is not JSON"
    
    missing_keys = [key for key in expected_keys if key not in json_data]
    assert not missing_keys, (
        f"JSON response is missing keys: {missing_keys}. "
        f"Available keys: {list(json_data.keys())}"
    )


def assert_form_error(response, field_name, error_message=None):
    """
    Assert that form has validation error for field.
    
    Args:
        response: Flask test response object
        field_name: Name of form field with error
        error_message: Optional specific error message to check
    """
    response_data = response.data.decode("utf-8") if isinstance(response.data, bytes) else response.data
    
    # Check for field name in error context
    assert field_name in response_data, (
        f"Field '{field_name}' not found in response (no error shown)"
    )
    
    if error_message:
        assert error_message in response_data, (
            f"Error message '{error_message}' not found for field '{field_name}'"
        )


def assert_model_attributes(instance, **expected_attrs):
    """
    Assert that model instance has expected attribute values.
    
    Args:
        instance: Model instance to check
        **expected_attrs: Keyword arguments of expected attribute values
    """
    for attr, expected_value in expected_attrs.items():
        actual_value = getattr(instance, attr, None)
        assert actual_value == expected_value, (
            f"Expected {instance.__class__.__name__}.{attr} = {expected_value}, "
            f"but got {actual_value}"
        )


def assert_file_exists(file_path):
    """
    Assert that file exists at given path.
    
    Args:
        file_path: Path to file (string or Path object)
    """
    from pathlib import Path
    
    path = Path(file_path)
    assert path.exists(), f"File not found: {file_path}"
    assert path.is_file(), f"Path is not a file: {file_path}"


def assert_file_content(file_path, expected_content):
    """
    Assert that file contains expected content.
    
    Args:
        file_path: Path to file
        expected_content: Expected content (string or bytes)
    """
    from pathlib import Path
    
    path = Path(file_path)
    assert_file_exists(path)
    
    mode = "rb" if isinstance(expected_content, bytes) else "r"
    with open(path, mode) as f:
        actual_content = f.read()
    
    assert actual_content == expected_content, (
        f"File content mismatch. Expected: {expected_content[:100]}, "
        f"Got: {actual_content[:100]}"
    )


def assert_raises_with_message(exception_class, message_pattern, callable_obj, *args, **kwargs):
    """
    Assert that callable raises exception with specific message pattern.
    
    Args:
        exception_class: Expected exception class
        message_pattern: Regex pattern or substring to match in exception message
        callable_obj: Function to call
        *args, **kwargs: Arguments to pass to callable
    """
    import re
    
    try:
        callable_obj(*args, **kwargs)
        raise AssertionError(f"Expected {exception_class.__name__} to be raised")
    except exception_class as e:
        error_message = str(e)
        if isinstance(message_pattern, str) and not message_pattern.startswith("^"):
            # Simple substring match
            assert message_pattern in error_message, (
                f"Expected exception message to contain '{message_pattern}', "
                f"but got '{error_message}'"
            )
        else:
            # Regex match
            assert re.search(message_pattern, error_message), (
                f"Expected exception message to match pattern '{message_pattern}', "
                f"but got '{error_message}'"
            )
