from process_navigator.utils.decorators import login_required, session_keys

from flask import render_template, Blueprint, request, session, redirect, url_for
from .forms import (
    IndexForm,
    ProcessPathForm,
)
from .models import PathData

from process_navigator.extensions.database import db
from process_navigator.models.process import ProcessMethodPart

# set up blueprint
bp = Blueprint("cauldron", __name__, url_prefix="/cauldron")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = IndexForm()

    if form.start.data:
        session["security_keys"].append("cauldron_start")
        session.modified = True
        return redirect(url_for("cauldron.process_path"))

    return render_template("cauldron/index.html", form=form)


@bp.route("/process_path", methods=["GET", "POST"])
@login_required
@session_keys({"cauldron_start": "cauldron.index"})
def process_path():
    form = ProcessPathForm()

    # this route is built upon a nest fieldlist form, so each post will need to enumrate through the form fields
    # we grab the enumeration and check if any of the buttons for that index  are submitted

    if request.method == "POST":
        # deal with ProcessPathForm

        # add Parent Entity
        if form.add_parent_entity.data:
            print("Adding a parent entity")
            form.parent_entities.append_entry()
        # add another process
        if form.add_process.data:
            form.processes.append_entry()

        # deal with ProcessForm
        for process_index, process in enumerate(form.processes, start=1):
            # delete process (onlu if there is more than one process)

            if process_index > 1 and process.delete_process.data:
                form.processes.pop_entry()

            # add another process step
            if process.add_process_step.data:
                print("Adding a process step")
                process.process_steps.append_entry()
                process.open_details = True

            # deal with ProcessStepForm
            for process_step_index, process_step in enumerate(
                process.process_steps, start=1
            ):
                # select Process Method, this will give choice of process method parts
                # the process method parts wil only appear when a Process Method is selected
                if process_step.select_method.data:
                    process_step.process_method_part.query = db.session.execute(
                        db.select(ProcessMethodPart).filter(
                            ProcessMethodPart.process_method_id
                            == process_step.process_method.data.id
                        )
                    ).scalars()

                    # set the open details to true
                    process_step.open_details = True
                    process.open_details = True

                # delete proccess step
                if process_step_index > 1:
                    if process_step.delete_process_step.data:
                        process.process_steps.pop_entry()

                # deal with parameters
                if process_step.add_parameter.data:
                    process_step.parameters.append_entry()

                    # set the open details to true
                    process.open_details = True
                    process_step.open_details = True
                    process_step.open_parameter_details = True

                if process_step.remove_parameter.data:
                    process_step.parameters.pop_entry()
                    process.open_details = True
                    process_step.open_details = True

                # deal with parameter values
                for parameter_index, parameter in enumerate(process_step.parameters):
                    if parameter.add_value.data:
                        parameter.values.append_entry()
                        # set the open details to true
                        process.open_details = True
                        process_step.open_details = True
                        process_step.open_parameter_details = True

                    if parameter.delete_value.data:
                        parameter.values.pop_entry()
                        # set the open details to true
                        process.open_details = True
                        process_step.open_details = True
                        process_step.open_parameter_details = True

                # deal with inputs
                if process_step.add_input.data:
                    process_step.inputs.append_entry()
                    # set the open details to true
                    process.open_details = True
                    process_step.open_details = True
                    process_step.open_input_details = True

                if process_step.remove_input.data:
                    process_step.inputs.pop_entry()

                # deal with input values
                for input_index, input in enumerate(process_step.inputs):
                    if input.add_value.data:
                        input.values.append_entry()
                        # set the open details to true
                        process.open_details = True  # type: ignore
                        process_step.open_details = True
                        process_step.open_input_details = True

                    if input.delete_value.data:
                        input.values.pop_entry()
                        # set the open details to true
                        process.open_details = True
                        process_step.open_details = True
                        process_step.open_input_details = True

    # provide current information about the length of the paths and the number of different paths
    #  we expect different paths if the user is using design of experiments

    path_data = PathData(form)

    return render_template("cauldron/process_path.html", form=form, path_data=path_data)
