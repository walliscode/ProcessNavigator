from .utils import provide_stacked_response
from process_navigator.extensions.database import db
from process_navigator.models import User


# redirects to login page is user is not logged in (or registered)
def test_index_get(client, route_options):
    # set up paths for this test to follow
    paths = ["home_index_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"


def test_register_get(client, route_options):
    # set up paths for this test to follow
    paths = ["register_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert b"Registration" in response.data


def test_register_user(client, route_options, test_app):
    # set up paths for this test to follow
    paths = ["register_user"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200

    html_data = [
        "User test user was registered successfully with email test_user@astrea-bio.com"
    ]
    for data in html_data:
        assert data.encode() in response.data

    # database checks
    with test_app.app_context():
        user_query = db.session.execute(
            db.select(User).filter(User.email == "test_user@astrea-bio.com")
        ).scalar_one_or_none()
    assert user_query is not None


def test_login_get(client, route_options):
    # set up paths for this test to follow
    paths = ["login_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["Login"]
    for data in html_data:
        assert data.encode() in response.data


def test_login_user(client, route_options):
    # set up paths for this test to follow
    paths = ["login_user"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["User with email test_user@astrea-bio.com does not exist."]
    for data in html_data:
        assert data.encode() in response.data


def test_login_user_bad_password(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user_bad_password"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["Incorrect password for user test_user@astrea-bio.com."]
    for data in html_data:
        assert data.encode() in response.data


def test_login_user_success(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
