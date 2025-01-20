from process_navigator.extensions.database import db
from process_navigator.models.admin import User


def test_user_model(test_app):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the name, email, hashed_password, is_admin, is_superuser, is_active, created_at, updated_at fields are defined correctly
    """

    # first check database is empty

    with test_app.app_context():
        assert db.session.execute(db.select(User)).first() is None

        # create a new User

        new_user = User(
            first_name="John",
            last_name="Doe",
            email="j.doe@astrea-bio.com",
            password="password",
        )

        db.session.add(new_user)
        db.session.commit()

        # check the User is created and added to the database

        user_query = db.session.execute(db.select(User)).scalar()
        assert user_query is not None
        assert user_query.id == 1
        assert user_query.first_name == "John"
        assert user_query.last_name == "Doe"
        assert user_query.email == "j.doe@astrea-bio.com"
        assert user_query.password == "password"
        assert not user_query.is_admin
        assert not user_query.is_superuser
        assert user_query.is_active

        # check that only one User is created_at
        users_query = db.session.execute(db.select(User)).all()
        assert len(users_query) == 1
