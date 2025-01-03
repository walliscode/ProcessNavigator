from flask import flash, redirect, render_template, session, url_for

from process_navigator.data import bp
from process_navigator.extensions import db
from process_navigator.models.process import ProcessMethod, ProcessMethodPart
from process_navigator.utils.decorators import login_required, session_keys
from process_navigator.utils.file_handling import save_file

from .forms import (
    AddMethodForm,
    CurrentMethodsForm,
    DeleteProcessMethodForm,
    MethodForm,
)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("data/index.html")


@bp.route("/process_methods", methods=["GET", "POST"])
@login_required
def process_methods():
    form = MethodForm()
    form2 = CurrentMethodsForm()

    if form.add_method.data:
        # add security key to session of "add_method"
        session["security_keys"].append("add_process_method")
        # session does not automatically update when a list is modified (a mutable object)
        session.modified = True
        return redirect(url_for("data.add_process_method"))

    if form.delete_method.data:
        # add security key to session of "delete_method"
        session["security_keys"].append("delete_process_method")
        # session does not automatically update when a list is modified (a mutable object)
        session.modified = True
        return redirect(url_for("data.delete_process_method"))
    return render_template("data/process_methods.html", form=form, form2=form2)


@bp.route("/add_process_method", methods=["GET", "POST"])
@login_required
@session_keys({"add_process_method": "data.process_methods"})
def add_process_method():
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
            return redirect(url_for("data.add_process_method"))

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
            session["security_keys"].remove("add_process_method")
            session.modified = True
            return redirect(url_for("data.process_methods"))

    return render_template("data/add_process_method.html", form=form)


@bp.route("/delete_process_method", methods=["GET", "POST"])
@login_required
@session_keys({"delete_process_method": "data.process_methods"})
def delete_process_method():
    form = DeleteProcessMethodForm()

    if form.delete_method.data:
        process_method = form.process_method_list.data

        # delete the process method and process method parts from the database
        db.session.delete(process_method)
        db.session.commit()

        # check if the process method and process method parts have been deleted from the database, return a message on results of the database commit
        process_method_query = db.session.execute(
            db.select(ProcessMethod).filter(ProcessMethod.name == process_method.name)
        ).scalar()

        # if present return an error message
        if process_method_query:
            message = "Process Method {name} and Process Method Parts {parts} not deleted from database".format(
                name=process_method.name,
                parts=[part.name for part in process_method.process_method_parts],
            )
            flash(message)
            return redirect(url_for("data.delete_process_method"))

        elif not process_method_query:
            message = "Process Method {name} and Process Method Parts {parts} deleted from database".format(
                name=process_method.name,
                parts=[part.name for part in process_method.process_method_parts],
            )
            flash(message)

            # remove security key from session and redirect to the methods page
            session["security_keys"].remove("delete_process_method")
            session.modified = True
            return redirect(url_for("data.process_methods"))
    return render_template("data/delete_process_method.html", form=form)
