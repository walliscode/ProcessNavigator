from flask import render_template

from process_navigator.data import bp
from process_navigator.utils.decorators import login_required

from .forms import MethodForm


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("data/index.html")


@bp.route("/methods", methods=["GET", "POST"])
@login_required
def methods():
    form = MethodForm()

    return render_template("data/methods.html", form=form)
