from process_navigator.extensions import db
from process_navigator.models.admin import User


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


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
