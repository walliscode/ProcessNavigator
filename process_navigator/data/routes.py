from flask import flash, redirect, render_template, session, url_for

from process_navigator.data import bp
from process_navigator.extensions import db
from process_navigator.models.analysis import AnalysisMethod, AnalysisMethodPart
from process_navigator.models.process import ProcessMethod, ProcessMethodPart
from process_navigator.models.units import BaseUnit, Unit, UnitCombination, UnitModifier
from process_navigator.utils.decorators import login_required, session_keys
from process_navigator.utils.file_handling import save_file

from .forms import (
    AddAnalysisMethodForm,
    EditAnalysisMethodForm,
    AddMethodForm,
    AddUnitForm,
    AnalysisMethodForm,
    BaseUnitForm,
    CurrentMethodsForm,
    CurrentUnitsForm,
    DeleteProcessMethodForm,
    MethodForm,
    UnitModifierForm,
    UnitsForm,
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
            parts = ", ".join(
                [part.name for part in process_method_query.process_method_parts]
            )

            message = "Process Method {name} and Process Method Parts {parts} not deleted from database".format(
                name=process_method.name,
                parts=parts,
            )
            flash(message)
            return redirect(url_for("data.delete_process_method"))

        elif not process_method_query:
            parts = ", ".join(
                [part.name for part in process_method.process_method_parts]
            )

            message = "Process Method {name} and Process Method Parts {parts} deleted from database".format(
                name=process_method.name,
                parts=parts,
            )
            flash(message)

            # remove security key from session and redirect to the methods page
            session["security_keys"].remove("delete_process_method")
            session.modified = True
            return redirect(url_for("data.process_methods"))
    return render_template("data/delete_process_method.html", form=form)


"""
The next routes deal with adding, editing and deleting Units from the database
"""


@bp.route("/units", methods=["GET", "POST"])
@login_required
def units():
    form = UnitsForm()
    form2 = CurrentUnitsForm()

    symbol_query = db.session.execute(db.select(Unit)).first()
    test_text = symbol_query
    if form.add_units.data:
        # add security key to session of "add_units"
        session["security_keys"].append("add_unit")
        # session does not automatically update when a list is modified (a mutable object)
        session.modified = True
        return redirect(url_for("data.add_unit"))
    return render_template(
        "data/units.html", form=form, form2=form2, test_text=test_text
    )


@bp.route("/add_unit", methods=["GET", "POST"])
@login_required
@session_keys({"add_unit": "data.units"})
def add_unit():
    form = AddUnitForm()

    if form.add_unit_part.data:
        # adds another entry to the unit_combinations form
        form.unit_combinations.append_entry()

    if form.add_unit.data:
        # first check the unit by name whether it already exists in the database
        unit_query = db.session.execute(
            db.select(Unit).filter(Unit.name == form.unit_name.data)
        ).scalar()

        if unit_query is not None:
            message = "Unit {name} already exists".format(name=form.unit_name.data)
            flash(message)
            return redirect(url_for("data.add_unit"))

        # check whether the unit combination is unique
        # if at any point a unit combination is not found then the unit combination is unique
        unit_combination_is_unique = False
        for unit_combination in form.unit_combinations:
            unit_combination_query = db.session.execute(
                db.select(UnitCombination)
                .filter(
                    UnitCombination.base_unit_id == unit_combination.base_unit.data.id
                )
                .filter(
                    UnitCombination.unit_modifier_id
                    == unit_combination.unit_modifier.data.id
                )
                .filter(UnitCombination.exponent == unit_combination.exponent.data)
            ).scalar()

            if not unit_combination_query:
                unit_combination_is_unique = True
                break

        if not unit_combination_is_unique:
            message = "That combination of unit parts already exists"
            flash(message)
            return redirect(url_for("data.add_unit"))

        # if the unit_combination is unique then add the unit to the database
        if unit_combination_is_unique:
            # first add the Unit, the symbol is generated from the Unit Parts
            new_unit = Unit(
                name=form.unit_name.data.__str__(),
            )

            db.session.add(new_unit)
            db.session.commit()

            # now add the unit combinations to the database

            for unit_combination in form.unit_combinations:
                new_unit_combination = UnitCombination(
                    unit_id=new_unit.id,
                    unit=new_unit,
                    base_unit_id=unit_combination.base_unit.data.id,
                    unit_modifier_id=unit_combination.unit_modifier.data.id,
                    exponent=unit_combination.exponent.data,
                    base_unit=unit_combination.base_unit.data,
                    unit_modifier=unit_combination.unit_modifier.data,
                )

                db.session.add(new_unit_combination)

            db.session.commit()

            # check if the unit has been added to the database
            unit_query = db.session.execute(
                db.select(Unit).filter(Unit.name == form.unit_name.data)
            ).scalar()

            # return message depending on result of the unit_query
            if unit_query:
                message = "Unit {name} added to database".format(name=unit_query.name)
                flash(message)

                # remove security key from session and redirect to the units page
                session["security_keys"].remove("add_unit")
                session.modified = True
                return redirect(url_for("data.units"))

            elif not unit_query:
                message = "Unit {name} not added to database".format(
                    name=form.unit_name.data
                )
                flash(message)
                return redirect(url_for("data.add_unit"))

    return render_template("data/add_unit.html", form=form)


@bp.route("/base_units", methods=["GET", "POST"])
@login_required
def base_units():
    form = BaseUnitForm()

    if form.add_base_unit.data:
        # check whether the base unit already exists in the database
        base_unit_query = db.session.execute(
            db.select(BaseUnit).filter(BaseUnit.name == form.unit_name.data)
        ).scalar()

        if base_unit_query:
            message = "Base Unit {name} already exists".format(name=form.unit_name.data)
            flash(message)
            return redirect(url_for("data.base_units"))

        new_base_unit = BaseUnit(
            name=form.unit_name.data.__str__(), symbol=form.unit_symbol.data.__str__()
        )

        db.session.add(new_base_unit)
        db.session.commit()

        new_base_unit_query = db.session.execute(
            db.select(BaseUnit).filter(BaseUnit.name == form.unit_name.data)
        ).scalar()

        if new_base_unit_query:
            message = "Base Unit {name} added to database".format(
                name=new_base_unit.name
            )
            flash(message)
            return redirect(url_for("data.base_units"))

        elif not new_base_unit_query:
            message = "Base Unit {name} not added to database".format(
                name=new_base_unit.name
            )
            flash(message)
            return redirect(url_for("data.base_units"))

    if form.delete_base_unit.data:
        base_unit = form.current_base_units.data

        db.session.delete(base_unit)
        db.session.commit()

        base_unit_query = db.session.execute(
            db.select(BaseUnit).filter(BaseUnit.name == base_unit.name)
        ).scalar()

        if base_unit_query:
            message = "Base Unit {name} not deleted from database".format(
                name=base_unit.name
            )
            flash(message)
            return redirect(url_for("data.base_units"))

        elif not base_unit_query:
            message = "Base Unit {name} deleted from database".format(
                name=base_unit.name
            )
            flash(message)
            return redirect(url_for("data.base_units"))

    return render_template("data/base_units.html", form=form)


@bp.route("/unit_modifiers", methods=["GET", "POST"])
@login_required
def unit_modifiers():
    print("test_text_1")
    form = UnitModifierForm()

    print("test_text")
    if form.add_unit_modifier.data:
        # check whether the unit modifier already exists in the database
        unit_modifier_query = db.session.execute(
            db.select(UnitModifier).filter(UnitModifier.name == form.modifier_name.data)
        ).scalar()

        if unit_modifier_query:
            message = "Unit Modifier {name} already exists".format(
                name=form.modifier_name.data
            )
            flash(message)
            return redirect(url_for("data.unit_modifiers"))

        new_unit_modifier = UnitModifier(
            name=form.modifier_name.data.__str__(),
            symbol=form.modifier_symbol.data.__str__(),
            multiplier=form.modifier_multiplier.data,
        )

        db.session.add(new_unit_modifier)
        db.session.commit()

        new_unit_modifier_query = db.session.execute(
            db.select(UnitModifier).filter(UnitModifier.name == form.modifier_name.data)
        ).scalar()

        if new_unit_modifier_query:
            message = "Unit Modifier {name} added to database".format(
                name=new_unit_modifier.name
            )
            flash(message)
            return redirect(url_for("data.unit_modifiers"))

        elif not new_unit_modifier_query:
            message = "Unit Modifier {name} not added to database".format(
                name=new_unit_modifier.name
            )
            flash(message)
            return redirect(url_for("data.unit_modifiers"))

    if form.delete_unit_modifier.data:
        unit_modifier = form.current_unit_modifiers.data

        db.session.delete(unit_modifier)
        db.session.commit()

        unit_modifier_query = db.session.execute(
            db.select(UnitModifier).filter(UnitModifier.name == unit_modifier.name)
        ).scalar()

        if unit_modifier_query:
            message = "Unit Modifier {name} not deleted from database".format(
                name=unit_modifier.name
            )
            flash(message)
            return redirect(url_for("data.unit_modifiers"))

        elif not unit_modifier_query:
            message = "Unit Modifier {name} deleted from database".format(
                name=unit_modifier.name
            )
            flash(message)
            return redirect(url_for("data.unit_modifiers"))

    return render_template("data/unit_modifiers.html", form=form)


@bp.route("/analysis_methods", methods=["GET", "POST"])
@login_required
def analysis_methods():
    form = AnalysisMethodForm()

    # add security key to session of "add_analysis_method" and redirect to the add_analysis_method page
    if form.add_analysis_method.data:
        session["security_keys"].append("add_analysis_method")
        session.modified = True
        return redirect(url_for("data.add_analysis_method"))

    if form.edit_analysis_method.data:
        session["security_keys"].append("edit_analysis_method")
        session.modified = True
        return redirect(url_for("data.edit_analysis_method"))

    return render_template("data/analysis_methods.html", form=form)


@bp.route("/add_analysis_method", methods=["GET", "POST"])
@login_required
@session_keys({"add_analysis_method": "data.analysis_methods"})
def add_analysis_method():
    form = AddAnalysisMethodForm()

    # add extra method part field if the add_method_part button is clicked
    if form.add_method_part.data:
        form.method_parts.append_entry()

    # remove method part field if the remove_method_part button is clicked
    if form.remove_method_part.data:
        form.method_parts.pop_entry()

    # now to add method to the database
    if form.add_method.data:
        # perform error checking to make sure the AnalysisMethod do not already exist
        analysis_method_query = db.session.execute(
            db.select(AnalysisMethod).filter(
                AnalysisMethod.name == form.method_name.data
            )
        ).scalar()

        if analysis_method_query:
            message = "Analysis Method {name} already exists".format(
                name=form.method_name.data
            )
            flash(message)
            return redirect(url_for("data.add_analysis_method"))

        # save file to the file storage system and get the new file name
        method_file = save_file(form.method_file.data)

        # add the analysis method to the database, this will give the analysis method an id
        new_method = AnalysisMethod(
            name=form.method_name.data.__str__(),
            description=form.method_description.data.__str__(),
            file_name=method_file,
        )
        db.session.add(new_method)

        # cycle through analysis method parts and add to the database
        for method_part in form.method_parts:
            new_method_part = AnalysisMethodPart(
                name=method_part.method_part_name.data,
                unit_id=method_part.method_part_unit.data.id,
                data_type=method_part.data_type.data,
                analysis_method_id=new_method.id,
                analysis_method=new_method,
            )
            db.session.add(new_method_part)

        db.session.commit()

        # now check the data has been correctly added to the database, dedirect upon success

        method_added_query = db.session.execute(
            db.select(AnalysisMethod).filter(AnalysisMethod.id == new_method.id)
        ).scalar()

        if method_added_query is not None:
            # check new_method parts have been added are linked to the AnalysisMethod
            if method_added_query.analysis_method_parts is not None:
                message = "Analysis Method {name} and Analysis Method Parts {parts} added to database".format(
                    name=method_added_query.name,
                    parts=", ".join(
                        [part.name for part in method_added_query.analysis_method_parts]
                    ),
                )

                flash(message)
                return redirect(url_for("data.analysis_methods"))

            else:
                message = "Analysis Method {name} added to database, but Analysis Method Parts not added. Please edit or delete method_added_query".format(
                    name=method_added_query.name
                )
                return redirect(url_for("data.analysis_methods"))
        else:
            message = "Analysis Method {name} not added to database".format(
                name=new_method.name
            )

            flash(message)
            return redirect(url_for("data.add_analysis_method"))

    return render_template("data/add_analysis_method.html", form=form)


@bp.route("/edit_analysis_method", methods=["GET", "POST"])
@login_required
@session_keys({"edit_analysis_method": "data.analysis_methods"})
def edit_analysis_method():
    form = EditAnalysisMethodForm()

    # once analytical method is selected to edit, populate the form with data and add correct session keys
    if form.select_method.data:
        session["analytical_method"] = {}
        session["analytical_method"]["id"] = form.current_methods.data.id

        # prepopulate form data
        form.method_name.data = form.current_methods.data.name
        form.method_description.data = form.current_methods.data.description
        # for each method part on the AnalysisMethod object, create a Field and populate data

    if form.commit_changes.data:
        # get AnalysisMethod objcet from the database
        analysis_method = db.session.execute(
            db.select(AnalysisMethod).filter(
                AnalysisMethod.id == session["analytical_method"]["id"]
            )
        ).scalar_one()

        # modify the AnalysisMethod object with the form data
        analysis_method.name = form.method_name.data
        analysis_method.description = form.method_description.data

        if form.method_file.data:
            method_file = save_file(form.method_file.data)
            analysis_method.file_name = method_file

        # modify the AnalysisMethodParts
        for count, method_part in enumerate(analysis_method.analysis_method_parts):
            method_part.name = form.method_parts[count].method_part_name.data
            method_part.unit_id = form.method_parts[count].method_part_unit.data.id
            method_part.data_type = form.method_parts[count].data_type.data

        db.session.commit()

        # flash success message and clear relevant session keys and data, redirect to analysis_methods
        message = "Analysis Method {name} and Analysis Method Parts {parts} updated in database".format(
            name=analysis_method.name,
            parts=", ".join(
                [part.name for part in analysis_method.analysis_method_parts]
            ),
        )
        flash(message)
        session.pop("analytical_method")
        session["security_keys"].remove("edit_analysis_method")
        session.modified = True
        return redirect(url_for("data.analysis_methods"))

    # Check if a specific button inside the FieldList was pressed
    for index, method_part in enumerate(form.method_parts):
        if method_part.delete_method_part.data:
            print("delete test")
            print(index)

    """ 
    each time the method parts get deleted or new one added, we are going to do the datbase edits straight away.
    This is to prevent the order of the list getting muddled
    To aid this, at the end of each requset we are going to update the form method parts with the AnalysisMethod object
    """

    if "analytical_method" in session:
        # get fresh object from the database
        analysis_method = db.session.execute(
            db.select(AnalysisMethod).filter(
                AnalysisMethod.id == session["analytical_method"]["id"]
            )
        ).scalar_one()

        # set the number of form.method_parts to mactch the number of AnalysisMethodParts using pop/append_entry
        print("ANalysis Method Parts")
        print(len(analysis_method.analysis_method_parts))
        while len(form.method_parts) < len(analysis_method.analysis_method_parts):
            form.method_parts.append_entry()
            if len(form.method_parts) == len(analysis_method.analysis_method_parts):
                break

        while len(form.method_parts) > len(analysis_method.analysis_method_parts):
            form.method_parts.pop_entry()
            if len(form.method_parts) == len(analysis_method.analysis_method_parts):
                break

        # update the method parts in the form
        for count, method_part in enumerate(analysis_method.analysis_method_parts):
            form.method_parts[count].method_part_name.data = method_part.name
            form.method_parts[count].method_part_unit.data = method_part.unit_id
            form.method_parts[count].data_type.data = method_part.data_type

    return render_template("data/edit_analysis_method.html", form=form)
