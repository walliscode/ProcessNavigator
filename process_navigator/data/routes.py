from flask import flash, redirect, render_template, session, url_for

from process_navigator.data import bp
from process_navigator.extensions import db
from process_navigator.models.process import ProcessMethod, ProcessMethodPart
from process_navigator.models.units import BaseUnit, Unit, UnitCombination, UnitModifier
from process_navigator.utils.decorators import login_required, session_keys
from process_navigator.utils.file_handling import save_file

from .forms import (
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

            symbol = ""
            for unit_part in form.unit_combinations:
                symbol += unit_part.unit_modifier.data.symbol
                symbol += unit_part.base_unit.data.symbol
                symbol += "^"
                symbol += unit_part.exponent.data.__str__()

            html_symbol = ""

            for unit_part in form.unit_combinations:
                html_symbol += unit_part.unit_modifier.data.symbol
                html_symbol += unit_part.base_unit.data.symbol
                html_symbol += "<sup>"
                html_symbol += unit_part.exponent.data.__str__()
                html_symbol += "</sup>"

            new_unit = Unit(
                name=form.unit_name.data.__str__(),
                symbol=symbol,
                html_symbol=html_symbol,
            )

            db.session.add(new_unit)
            db.session.commit()

            # now add the unit combinations to the database

            for unit_combination in form.unit_combinations:
                new_unit_combination = UnitCombination(
                    unit_id=new_unit.id,
                    base_unit_id=unit_combination.base_unit.data.id,
                    unit_modifier_id=unit_combination.unit_modifier.data.id,
                    exponent=unit_combination.exponent.data,
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

        new_base_unit = BaseUnit(name=form.unit_name.data, symbol=form.unit_symbol.data)

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
    form = UnitModifierForm()

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
            symbol=form.modifier_symbol.data,
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

    return render_template("data/analysis_methods.html", form=form)
