"""
General test helper functions.

These functions provide common test operations and utilities.
"""

from pathlib import Path
import json


def provide_stacked_response(client, paths, route_options):
    """
    Execute a sequence of HTTP requests and return the final response.
    
    This helper simulates a user journey by executing multiple requests
    in sequence, maintaining session state between requests.
    
    Args:
        client: Flask test client
        paths: List of path names from route_options
        route_options: List of route configuration dictionaries
    
    Returns:
        Final response object from the last request
    
    Example:
        paths = ["register_user", "login_user", "data_index_get"]
        response = provide_stacked_response(client, paths, route_options)
    """
    response = client.get("/")
    
    for path in paths:
        # Find the relevant path in the route_options
        route_info = {}
        for route in route_options:
            if path in route["name"]:
                route_info = route
                break
        
        if not route_info:
            raise ValueError(f"Path '{path}' not found in route_options")
        
        method = route_info["method"]
        route = route_info["route"]
        data = route_info.get("data", {})
        
        # Handle file uploads if present
        if "file" in data:
            test_files = Path.cwd() / "tests" / "data" / "test_files"
            new_key = data["file"]["field_name"]
            data[new_key] = (test_files / data["file"]["file_name"]).open("rb")
        
        # Execute request
        if method == "GET":
            if "follow_redirects" in route_info:
                response = client.get(route, follow_redirects=True)
            else:
                response = client.get(route)
        elif method == "POST":
            if "follow_redirects" in route_info:
                response = client.post(route, data=data, follow_redirects=True)
            else:
                response = client.post(route, data=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    
    return response


def login_user(client, email="test_user@astrea-bio.com", password="testpassword"):
    """
    Helper to log in a user.
    
    Args:
        client: Flask test client
        email: User email
        password: User password
    
    Returns:
        Response object from login request
    """
    return client.post(
        "/login",
        data={"email": email, "password": password, "submit": True},
        follow_redirects=True
    )


def register_user(client, email="test@example.com", password="password",
                 first_name="Test", last_name="User"):
    """
    Helper to register a new user.
    
    Args:
        client: Flask test client
        email: User email
        password: User password
        first_name: User's first name
        last_name: User's last name
    
    Returns:
        Response object from registration request
    """
    return client.post(
        "/register",
        data={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "submit": True
        },
        follow_redirects=True
    )


def register_and_login(client, email="test@example.com", password="password"):
    """
    Helper to register and login a user in one step.
    
    Args:
        client: Flask test client
        email: User email
        password: User password
    
    Returns:
        Tuple of (register_response, login_response)
    """
    register_response = register_user(client, email=email, password=password)
    login_response = login_user(client, email=email, password=password)
    return register_response, login_response


def load_json_data(filename, data_dir="data"):
    """
    Load JSON data from tests data directory.
    
    Args:
        filename: Name of JSON file (e.g., 'route_options.json')
        data_dir: Subdirectory under tests/ (default: 'data')
    
    Returns:
        Parsed JSON data
    """
    data_path = Path.cwd() / "tests" / data_dir / filename
    with open(data_path) as f:
        return json.load(f)


def load_test_scenario(scenario_name):
    """
    Load test scenario from scenarios directory.
    
    Args:
        scenario_name: Name of scenario file (e.g., 'edge_cases.json')
    
    Returns:
        Parsed scenario data
    """
    return load_json_data(scenario_name, data_dir="data/scenarios")


def get_route_by_name(route_name, route_options):
    """
    Get route configuration by name from route_options.
    
    Args:
        route_name: Name of the route
        route_options: List of route configurations
    
    Returns:
        Route configuration dictionary
    
    Raises:
        ValueError: If route not found
    """
    for route in route_options:
        if route["name"] == route_name:
            return route
    
    raise ValueError(f"Route '{route_name}' not found in route_options")


def create_temp_file(content, filename="test_file.txt", binary=False):
    """
    Create a temporary file for testing.
    
    Args:
        content: File content (string or bytes)
        filename: Name of the file
        binary: Whether to write in binary mode
    
    Returns:
        Path to created file
    """
    from tempfile import mkdtemp
    
    temp_dir = Path(mkdtemp())
    temp_file = temp_dir / filename
    
    mode = "wb" if binary else "w"
    with open(temp_file, mode) as f:
        f.write(content)
    
    return temp_file


def cleanup_temp_files(temp_path):
    """
    Clean up temporary files and directories.
    
    Args:
        temp_path: Path to temporary file or directory
    """
    import shutil
    
    path = Path(temp_path)
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def wait_for_condition(condition_func, timeout=5, interval=0.1):
    """
    Wait for a condition to become true.
    
    Useful for testing asynchronous operations.
    
    Args:
        condition_func: Function that returns True when condition is met
        timeout: Maximum time to wait in seconds
        interval: Time between checks in seconds
    
    Returns:
        True if condition met, False if timeout
    """
    import time
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    
    return False


def extract_csrf_token(response):
    """
    Extract CSRF token from HTML response.
    
    Args:
        response: Flask test response object
    
    Returns:
        CSRF token string or None if not found
    """
    import re
    
    response_data = response.data.decode("utf-8")
    match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', response_data)
    
    if match:
        return match.group(1)
    
    return None


def get_session_value(client, key, default=None):
    """
    Get value from session.
    
    Args:
        client: Flask test client
        key: Session key
        default: Default value if key not found
    
    Returns:
        Session value or default
    """
    with client.session_transaction() as session:
        return session.get(key, default)


def set_session_value(client, key, value):
    """
    Set value in session.
    
    Args:
        client: Flask test client
        key: Session key
        value: Value to set
    """
    with client.session_transaction() as session:
        session[key] = value


def clear_session(client):
    """
    Clear all session data.
    
    Args:
        client: Flask test client
    """
    with client.session_transaction() as session:
        session.clear()


def get_flash_messages(client):
    """
    Get flash messages from session.
    
    Args:
        client: Flask test client
    
    Returns:
        List of flash message tuples (category, message)
    """
    with client.session_transaction() as session:
        flashes = session.get("_flashes", [])
        return flashes


def count_queries(db_session):
    """
    Context manager to count database queries.
    
    Useful for performance testing.
    
    Usage:
        with count_queries(db_session) as counter:
            # do database operations
        print(f"Executed {counter.count} queries")
    """
    class QueryCounter:
        def __init__(self):
            self.count = 0
        
        def __call__(self, *args, **kwargs):
            self.count += 1
    
    counter = QueryCounter()
    # This would need to be implemented with SQLAlchemy event listeners
    # For now, it's a placeholder
    return counter


def validate_json_schema(data, schema):
    """
    Validate data against JSON schema.
    
    Args:
        data: Data to validate
        schema: JSON schema dictionary
    
    Raises:
        jsonschema.ValidationError: If validation fails
    """
    import jsonschema
    jsonschema.validate(data, schema)


def compare_dicts(dict1, dict2, ignore_keys=None):
    """
    Compare two dictionaries, optionally ignoring certain keys.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        ignore_keys: List of keys to ignore in comparison
    
    Returns:
        True if dictionaries are equal (ignoring specified keys)
    """
    if ignore_keys is None:
        ignore_keys = []
    
    keys1 = set(dict1.keys()) - set(ignore_keys)
    keys2 = set(dict2.keys()) - set(ignore_keys)
    
    if keys1 != keys2:
        return False
    
    for key in keys1:
        if dict1[key] != dict2[key]:
            return False
    
    return True


def generate_random_email():
    """
    Generate a random email address for testing.
    
    Returns:
        Random email string
    """
    import random
    import string
    
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@test.example.com"


def generate_random_string(length=10, chars=None):
    """
    Generate a random string for testing.
    
    Args:
        length: Length of string
        chars: Characters to use (default: ascii letters and digits)
    
    Returns:
        Random string
    """
    import random
    import string
    
    if chars is None:
        chars = string.ascii_letters + string.digits
    
    return ''.join(random.choices(chars, k=length))
