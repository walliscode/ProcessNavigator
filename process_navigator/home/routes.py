import logging
import eralchemy2


# get bp object and use as decorator
from process_navigator.home import bp
from process_navigator.models import db

# import flask functionality
from flask import render_template, current_app


# render_templates looks for templates in the templates folder


@bp.route("/")
def index():

    return render_template("home/index.html")


@bp.route("/erdiagram")
def erdiagram():

    try:

        db_path = "sqlite:///instance/app.db"
        output_path = "process_navigator/static/images/erdiagram.png"

        # Log the paths being used
        current_app.logger.debug(f"Database path: {db_path}")
        current_app.logger.debug(f"Output path: {output_path}")

        # Render the ER diagram
        eralchemy2.render_er(db_path, output_path)

        # Log success
        current_app.logger.debug("ER diagram rendered successfully.")

    except Exception as e:
        # Log any exceptions with detailed information
        current_app.logger.error(f"Error rendering ER diagram: {e}", exc_info=True)
        return "An error occurred while generating the ER diagram.", 500

    return render_template("home/erdiagram.html")
