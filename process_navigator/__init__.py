# Import the Flask class from the flask module, which is the main class of the Flask framework

from flask import Flask

from process_navigator import data, home
from process_navigator.extensions import db, refresh_database_command


# create a create_app function that initializes the Flask application, we can add other logic depending on set up
def create_app(test_config=None):
    app = Flask(
        __name__, instance_relative_config=True
    )  # Create an instance of the Flask class and assign it to the variable app

    if test_config is None:
        app.config["SECRET_KEY"] = "dev"  # Set the secret key of the app to 'dev'
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "postgresql://processnavigator:test@localhost/processnavigator"
        )
    else:
        app.config.from_mapping(test_config)
    # register blueprints
    blueprint_list = [home.bp, data.bp]
    for blueprint in blueprint_list:
        app.register_blueprint(blueprint)
    # register extensions
    db.init_app(app)

    # register commands
    app.cli.add_command(refresh_database_command)

    return app
