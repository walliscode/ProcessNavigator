from flask import render_template

from process_navigator.data import bp
from process_navigator.utils.decorators import login_required


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("data/index.html")
