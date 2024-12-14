import pytest

# get imports from process_navigator
from process_navigator import create_app, db
from process_navigator.models.admin import User

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


# create a admin register and login fixture
@pytest.fixture
def admin_user(client, test_app):
    with test_app.app_context():
        admin = User(
            first_name="Fiber",
            last_name="Admin",
            email="fiber_admin@astrea-bio.com",
            password="admin",
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()

    client.post(
        "/login",
        data={
            "email": "fiber_admin@astrea-bio.com",
            "password": "admin",
            "submit": True,
        },
    )
