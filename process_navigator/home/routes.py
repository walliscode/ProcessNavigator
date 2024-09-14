# get bp object and use as decorator
from process_navigator.home import bp

# import flask functionality
from flask import render_template

# render_templates looks for templates in the templates folder

@bp.route('/')
def index():

    return render_template('home/index.html')