from flask import (
    Flask,
)  # Import the Flask class from the flask module, which is the main class of the Flask framework

# import blueprints
from process_navigator import home

# import extensions
from process_navigator.extensions import db
from process_navigator import models


# create a create_app function that initializes the Flask application, we can add other logic depending on set up
def create_app():
    app = Flask(
        __name__, instance_relative_config=True
    )  # Create an instance of the Flask class and assign it to the variable app
    app.config["SECRET_KEY"] = "dev"  # Set the secret key of the app to 'dev'
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///app.db"  # Set the database URI to a SQLite database named db.sqlite
    )
    # register blueprints
    app.register_blueprint(home.bp)

    # register extensions
    db.init_app(app)
    return app
