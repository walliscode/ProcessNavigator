import json
from pathlib import Path

import jsonschema
import pytest  # get imports from process_navigator

from process_navigator import create_app, db
from tests.load_data import load_test_data

# create a fixture to set up a temporary database for TESTING


@pytest.fixture
def test_app():
    # initialize the app with testing configuration
    test_app = create_app(test_config=True)

    with test_app.app_context():
        db.create_all()

        # upload test data to the database
        test_data_path = Path.cwd() / "tests" / "data" / "test_data.json"
        with open(test_data_path) as test_data:
            test_data = json.load(test_data)
            load_test_data(json_data=test_data, db=db)

    yield test_app
    with test_app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


"""
The following fixture will be check the json test data against provided schema. By using autouse this is automatically run even if no test requests it directly.
The json and its schem pair have been added to the json_schema_pairs list. This is then passed as a parameter to the fixture.
"""

json_schema_pairs = [
    ("route_options.json", "route_options_schema.json"),
    ("user_paths.json", "user_paths_schema.json"),
]


@pytest.fixture(scope="session", autouse=True, params=json_schema_pairs)
def validate_json(request):
    json_file = Path.cwd() / "tests" / "data" / request.param[0]
    schema_file = Path.cwd() / "tests" / "data" / "schema" / request.param[1]

    # check if the file exists and return error if it does not
    if not json_file.exists():
        raise FileNotFoundError(f"File not found: {json_file}")

    # check if the file exists and return error if it does not
    if not schema_file.exists():
        raise FileNotFoundError(f"File not found: {schema_file}")

    # check the json file conforms to expected schema using json module, exit if any errors are present, printing out the error
    with open(json_file) as file:
        json_data = json.load(file)

    with open(schema_file) as file:
        schema = json.load(file)

    try:
        jsonschema.validate(json_data, schema)
    except jsonschema.ValidationError as e:
        print(
            "for file: {json_file}, {message} at element {path}".format(
                json_file=json_file, message=e.message, path=e.path
            )
        )
        exit(1)


# load data from json file in tests\data\route_options.json using Pathlib
@pytest.fixture(scope="session")
def route_options():
    data_path = Path.cwd() / "tests" / "data"
    json_file = data_path / "route_options.json"

    with open(json_file) as file:
        route_options = json.load(file)
    return route_options


"""
Check user_paths actually exist in route_options.
"""


@pytest.fixture(scope="session", autouse=True)
def check_user_paths(route_options):
    data_path = Path.cwd() / "tests" / "data"
    json_file = data_path / "user_paths.json"

    with open(json_file) as file:
        user_paths = json.load(file)

    # for all user_paths, check that the paths are contained in the route_options
    # first get a list of all the paths in the route_options
    route_options_list = []
    for route in route_options:
        route_options_list.append(route["name"])

    # check that all paths in user_paths are in route_options
    for user_path in user_paths:
        for path in user_path["path"]:
            if path not in route_options_list:
                raise ValueError(f"Path {path} not found in route_options")

    return user_paths


"""
This next function will NOT be a fixture as it is being called directly by pytest.mark.parametrize. 
Building on this, it can also not rely on a fixture - this may be due to my coding skills or the way pytest works.
"""


def get_user_paths():
    data_path = Path.cwd() / "tests" / "data"
    user_paths_file = data_path / "user_paths.json"

    with open(user_paths_file) as file:
        user_paths = json.load(file)

    return user_paths
