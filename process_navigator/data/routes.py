from flask import flash, redirect, render_template, session, url_for

from process_navigator.data import bp
from process_navigator.extensions import db
from process_navigator.models.process import ProcessMethod, ProcessMethodPart
from process_navigator.utils.decorators import login_required, session_keys
from process_navigator.utils.file_handling import save_file

from .forms import AddMethodForm, CurrentMethodsForm, MethodForm


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("data/index.html")


@bp.route("/methods", methods=["GET", "POST"])
@login_required
def methods():
    form = MethodForm()
    form2 = CurrentMethodsForm()

    if form.add_method.data:
        # add security key to session of "add_method"
        session["security_keys"].append("add_method")
        # session does not automatically update when a list is modified (a mutable object)
        session.modified = True
        return redirect(url_for("data.add_method"))
    return render_template("data/methods.html", form=form, form2=form2)


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

    # when the add_method button is clicked, add the ProcessMethod and ProcessMethodParts to the database
    if form.add_method.data:
        # perform error checking to make sure the ProcessMethod do not already exist
        process_method_query = db.session.execute(
            db.select(ProcessMethod).filter(ProcessMethod.name == form.method_name.data)
        ).scalar()

        if process_method_query:
            message = "Process Method {name} already exists".format(
                name=form.method_name.data
            )
            flash(message)
            return redirect(url_for("data.add_method"))

        # save file to the file storage system and get the new file name
        method_file = save_file(form.method_file.data)
        # add the process method to the database, this will give the process method an id
        new_method = ProcessMethod(
            name=form.method_name.data.__str__(),
            description=form.method_description.data.__str__(),
            file_name=method_file,
        )
        db.session.add(new_method)

        # cycle through process method parts and add to the database
        for method_part in form.method_parts:
            new_method_part = ProcessMethodPart(
                name=method_part.method_part_name.data,
                process_method_id=new_method.id,
                process_method=new_method,
            )
            db.session.add(new_method_part)

        db.session.commit()

        # check if the process method and process method parts have been added to the database, return a message on results of the database commit
        process_method_query = db.session.execute(
            db.select(ProcessMethod).filter(ProcessMethod.name == form.method_name.data)
        ).scalar()

        if process_method_query:
            messsage = "Process Method {name} and Process Method Parts {parts} added to database".format(
                name=process_method_query.name,
                parts=[part.name for part in process_method_query.process_method_parts],
            )
            flash(messsage)

            # remove security key from session and redirect to the methods page
            session["security_keys"].remove("add_method")
            session.modified = True
            return redirect(url_for("data.methods"))

    return render_template("data/add_method.html", form=form)
