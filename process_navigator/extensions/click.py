from pathlib import Path
import json
import click
from flask import current_app
from tests.load_data import load_test_data
from .database import db

# create a function to drop and create the database using click, also emtpy file storage


@click.command("refresh-db")
def refresh_database_command():
    db.drop_all()
    db.create_all()
    # delete all files in the file storage system using Pathlib
    file_storage = Path(current_app.config["FILE_STORAGE"])
    file_list = file_storage.glob("*")
    for file in file_list:
        file.unlink()
    # load test data if test_data in app config
    if "TEST_DATA" in current_app.config:
        if current_app.config["TEST_DATA"]:
            # import test data json files
            # upload test data to the database
            test_data_path = Path.cwd() / "tests" / "data" / "test_data.json"
            with open(test_data_path) as test_data:
                test_data = json.load(test_data)
                load_test_data(json_data=test_data, db=db)

    click.echo("Database refreshed")
