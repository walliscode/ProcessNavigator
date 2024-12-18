# Import the Flask class from the flask module, which is the main class of the Flask framework

from pathlib import Path

from flask import Flask

from process_navigator import data, home
from process_navigator.extensions import db, refresh_database_command


# create a create_app function that initializes the Flask application, we can add other logic depending on set up
def create_app(test_config=False):
    app = Flask(
        __name__, instance_relative_config=True
    )  # Create an instance of the Flask class and assign it to the variable app

    # set up configuration
    if test_config:
        app.config.from_pyfile("testing_config.py")
        app.config["FILE_STORAGE"] = Path(app.instance_path) / "test_file_storage"
    else:
        # make sure to change this for production
        app.config.from_pyfile("development_config.py")
        app.config["FILE_STORAGE"] = Path(app.instance_path) / "file_storage"

    # ensure the instance folder exists
    if not Path(app.config["FILE_STORAGE"]).exists():
        Path(app.config["FILE_STORAGE"]).mkdir()
    # register blueprints
    blueprint_list = [home.bp, data.bp]
    for blueprint in blueprint_list:
        app.register_blueprint(blueprint)
    # register extensions
    db.init_app(app)

    # register commands
    app.cli.add_command(refresh_database_command)

    return app
