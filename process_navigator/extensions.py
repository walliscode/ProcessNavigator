from pathlib import Path

import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass


# Create an instance of the SQLAlchemy class and assign it to the variable db
# this will be our database "engine", options can be passed in here
db = SQLAlchemy(model_class=Base)


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
    click.echo("Database refreshed")
