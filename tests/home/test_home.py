import pytest
from flask import session

from process_navigator.extensions import db
from process_navigator.models.admin import User
from tests.conftest import get_user_paths


@pytest.mark.parametrize("user_path", get_user_paths())
def test_(client, route_options, user_path):
    # first get response object by looping through the user_path path
    response = client.get("/")

    for path in user_path["path"]:
        # find the relevenat path in the route_options
        route_info = {}
        for route in route_options:
            if path in route["name"]:
                route_info = route
                break

        method = route_info["method"]
        route = route_info["route"]
        data = route_info["data"]

        if method == "GET":
            response = client.get(route)
        elif method == "POST":
            response = client.post(route, data=data)

        else:
            raise ValueError("Invalid method")

    # assert the response status code
    assert response.status_code == user_path["assertions"]["status_code"]
    # assert the session data
    if "session" in user_path["assertions"]:
        for key, value in user_path["assertions"]["session"].items():
            assert session[key] == value

    # assert content in the response
    if "content" in user_path["assertions"]:
        for content in user_path["assertions"]["content"]:
            assert content.encode("utf-8") in response.data


def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_registatrion_form_submit(client, test_app):
    # check database is empty of users

    with test_app.app_context():
        query_result = db.session.execute(db.select(User)).all()

        assert len(query_result) == 0

    response = client.post(
        "/register",
        data={
            "first_name": "john",
            "last_name": "doe",
            "email": "j.doe@astrea-bio.com",
            "password": "password",
            "submit": True,
        },
    )

    assert response.status_code == 200

    with test_app.app_context():
        query_result = db.session.execute(
            db.select(User).filter(User.email == "j.doe@astrea-bio.com")
        ).scalar()

        assert query_result is not None

        # check user details

        assert query_result.first_name == "john"

        assert query_result.last_name == "doe"

        assert query_result.password == "password"

        # check default permissions

        assert not query_result.is_admin

        assert query_result.is_active

        assert not query_result.is_superuser


def test_login_page(client):
    response = client.get("/login")

    assert response.status_code == 200

    # check for form fields in response

    assert b"Email" in response.data

    assert b"Password" in response.data

    assert b"Login" in response.data


def test_login_form_submit_correct(client, test_app):
    with test_app.app_context():
        # add user to the database

        new_user = User(
            first_name="john",
            last_name="doe",
            email="j.doe@astrea-bio.com",
            password="password",
        )

        db.session.add(new_user)

        db.session.commit()

    response = client.post(
        "/login",
        data={
            "email": "j.doe@astrea-bio.com",
            "password": "password",
            "submit": True,
        },
    )

    # assert redirects to index page

    assert response.status_code == 302

    assert response.headers["Location"] == "/"


def test_login_form_submit_unregistered(client, test_app):
    with test_app.app_context():
        # add user to the database

        new_user = User(
            first_name="john",
            last_name="doe",
            email="j.doe@astrea-bio.com",
            password="password",
        )

        db.session.add(new_user)

        db.session.commit()

    with client:
        response = client.post(
            "/login",
            data={
                "email": "test@astrea-bio.com",
                "password": "password",
                "submit": True,
            },
        )

        assert response.status_code == 200

        # assert error messages are flashed

        assert b"User with email test@astrea-bio.com does not exist." in response.data
        assert "user" not in session

        assert "security_keys" not in session


def test_login_form_submit_wrong_password(client, test_app):
    with test_app.app_context():
        # add user to the database

        new_user = User(
            first_name="john",
            last_name="doe",
            email="j.doe@astrea-bio.com",
            password="password",
        )

        db.session.add(new_user)

        db.session.commit()

    with client:
        response = client.post(
            "/login",
            data={
                "email": "j.doe@astrea-bio.com",
                "password": "wrong_password",
                "submit": True,
            },
        )

        assert response.status_code == 200

        # assert error messages are flashed

        assert b"Incorrect password for user j.doe@astrea-bio.com" in response.data
        assert "user" not in session

        assert "security_keys" not in session
