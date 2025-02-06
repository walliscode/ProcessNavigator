from process_navigator.utils.decorators import login_required, session_keys

from flask import render_template, Blueprint

# set up blueprint
bp = Blueprint("cauldron", __name__, url_prefix="/cauldron")


@bp.route("/")
@login_required
def index():
    return render_template("cauldron/index.html")
