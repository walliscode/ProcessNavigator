import click
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# Create a base class for our models to inherit from, this is following the documentation from the flask_sqlalchemy website
class Base(DeclarativeBase, MappedAsDataclass):
    pass


# Create an instance of the SQLAlchemy class and assign it to the variable db
# this will be our database "engine", options can be passed in here
db = SQLAlchemy(model_class=Base)


# create a function to drop and create the database using click
@click.command("refresh-db")
def refresh_database_command():
    db.drop_all()
    db.create_all()
    click.echo("Database refreshed")
