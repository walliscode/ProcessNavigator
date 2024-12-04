import pytest

# get imports from process_navigator
from process_navigator import create_app


@pytest.fixture
def app():

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    yield app



