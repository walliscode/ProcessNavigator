# set up flask blueprint for "home" module
from flask import Blueprint

bp = Blueprint("home", __name__)

# Import the routes module from the home package
from process_navigator.home import routes
