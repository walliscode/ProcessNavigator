# set up flask blueprint for "data" module
from flask import Blueprint

bp = Blueprint("data", __name__, url_prefix="/data")

# Import the routes module from the data package
from process_navigator.data import routes
