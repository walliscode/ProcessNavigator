from flask import redirect, render_template, session, url_for

from process_navigator.data import bp
from process_navigator.models.process import ProcessMethod
from process_navigator.utils.decorators import login_required, session_keys

from .forms import AddMethodForm, MethodForm


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("data/index.html")


@bp.route("/methods", methods=["GET", "POST"])
@login_required
def methods():
    form = MethodForm()

    if form.add_method.data:
        # add security key to session of "add_method"
        session["security_keys"].append("add_method")
        # session does not automatically update when a list is modified (a mutable object)
        session.modified = True
        return redirect(url_for("data.add_method"))
    return render_template("data/methods.html", form=form)


@bp.route("/add_method", methods=["GET", "POST"])
@login_required
@session_keys({"add_method": "data.methods"})
def add_method():
    form = AddMethodForm()

    # add extra method part field if the add_method_part button is clicked
    if form.add_method_part.data:
        form.method_parts.append_entry()

    if form.remove_method_part.data:
        form.method_parts.pop_entry()

    return render_template("data/add_method.html", form=form)
