from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass


# Create an instance of the SQLAlchemy class and assign it to the variable db
# this will be our database "engine", options can be passed in here
db = SQLAlchemy(model_class=Base)
