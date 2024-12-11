import pytest

# get imports from process_navigator
from process_navigator import create_app, db

# create a fixture to set up a temporary database for TESTING


@pytest.fixture
def test_app():
    # initialize the app with testing configuration
    test_app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "SQLALCHEMY_DATABASE_URI": (
                "postgresql://processnavigator:test@localhost/processnavigator_test"
            ),
        }
    )

    with test_app.app_context():
        db.create_all()
    yield test_app
    with test_app.app_context():
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()
