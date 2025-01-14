from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    FieldList,
    FileField,
    FormField,
    IntegerField,
    StringField,
    SubmitField,
)
from wtforms.fields import SelectField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from process_navigator.extensions import db
from process_navigator.models.analysis import AnalysisMethod
from process_navigator.models.process import ProcessMethod, ProcessMethodPart
from process_navigator.models.units import BaseUnit, Unit, UnitModifier
from process_navigator.shared_data.enums import DataTypes


def get_current_units():
    return db.session.execute(db.select(Unit)).scalars()


class MethodForm(FlaskForm):
    add_method = SubmitField("Add Method")
    edit_method = SubmitField("Edit Method")
    delete_method = SubmitField("Delete Method")


def get_current_process_methods():
    return db.session.execute(db.select(ProcessMethod)).scalars()


def get_current_process_method_parts():
    return db.session.execute(db.select(ProcessMethodPart)).scalars()


class CurrentMethodsForm(FlaskForm):
    current_methods = QuerySelectField(
        "Current Methods",
        allow_blank=False,
        query_factory=get_current_process_methods,
    )


class AddMethodPartForm(FlaskForm):
    method_part_name = StringField("Method Part Name", validators=[InputRequired()])


class AddMethodForm(FlaskForm):
    method_name = StringField("Method Name", validators=[InputRequired()])
    method_description = StringField("Method Description", validators=[InputRequired()])
    method_parts = FieldList(FormField(AddMethodPartForm), min_entries=1)
    add_method_part = SubmitField("Add Method Part")
    remove_method_part = SubmitField("Remove Method Part")
    method_file = FileField("Method File", validators=[InputRequired()])
    add_method = SubmitField("Add Method")
    reset = SubmitField("Reset")


class DeleteProcessMethodForm(FlaskForm):
    process_method_list = QuerySelectField(
        "Process Method List",
        allow_blank=False,
        query_factory=get_current_process_methods,
    )
    process_method_part_list = QuerySelectField(
        "Process Method Part List",
        allow_blank=False,
        query_factory=get_current_process_method_parts,
    )
    delete_method = SubmitField("Delete Method")


def get_current_analytical_methods():
    return db.session.execute(db.select(AnalysisMethod)).scalars()


class AnalysisMethodForm(FlaskForm):
    add_analysis_method = SubmitField("Add Analysis Method")
    edit_analysis_method = SubmitField("Edit Analysis Method")
    delete_analysis_method = SubmitField("Delete Analysis Method")
    current_analysis_methods = QuerySelectField(
        "Current Analysis Methods",
        allow_blank=False,
        query_factory=get_current_analytical_methods,
    )


class AddAnalysisMethodPartForm(FlaskForm):
    method_part_name = StringField("Method Part Name", validators=[InputRequired()])
    method_part_unit = QuerySelectField(
        "Unit",
        allow_blank=False,
        query_factory=get_current_units,
    )
    data_type = SelectField(
        "Data Type",
        choices=[data_type.value for data_type in DataTypes],
    )


class AddAnalysisMethodForm(FlaskForm):
    method_name = StringField("Method Name", validators=[InputRequired()])
    method_description = StringField("Method Description", validators=[InputRequired()])
    method_parts = FieldList(FormField(AddAnalysisMethodPartForm), min_entries=1)
    add_method_part = SubmitField("Add Method Part")
    remove_method_part = SubmitField("Remove Method Part")
    method_file = FileField("Method File", validators=[InputRequired()])
    add_method = SubmitField("Add Method")


class UnitsForm(FlaskForm):
    add_units = SubmitField("Add Units")
    edit_units = SubmitField("Edit Units")
    delete_units = SubmitField("Delete Units")


class CurrentUnitsForm(FlaskForm):
    current_units = QuerySelectField(
        "Current Units",
        allow_blank=False,
        query_factory=get_current_units,
        get_label=lambda x: "{name} ({symbol})".format(name=x.name, symbol=x.symbol),
    )


def get_current_base_units():
    return db.session.execute(db.select(BaseUnit)).scalars()


class BaseUnitForm(FlaskForm):
    unit_name = StringField("Unit Name", validators=[InputRequired()])
    unit_symbol = StringField("Unit Symbol", validators=[InputRequired()])
    add_base_unit = SubmitField("Add Base Unit")

    current_base_units = QuerySelectField(
        "Current Base Units",
        allow_blank=False,
        query_factory=get_current_base_units,
        get_label=lambda x: "{name} ({symbol})".format(name=x.name, symbol=x.symbol),
    )

    delete_base_unit = SubmitField("Delete Base Unit")


def get_current_unit_modifiers():
    return db.session.execute(db.select(UnitModifier)).scalars()


class UnitModifierForm(FlaskForm):
    modifier_name = StringField("Modifier Name", validators=[InputRequired()])
    modifier_symbol = StringField("Modifier Symbol", validators=[InputRequired()])
    modifier_multiplier = DecimalField(
        "Modifier Multiplier", validators=[InputRequired()]
    )
    add_unit_modifier = SubmitField("Add Unit Modifier")

    current_unit_modifiers = QuerySelectField(
        "Current Unit Modifiers",
        allow_blank=False,
        query_factory=get_current_unit_modifiers,
        get_label=lambda x: "{name} ({symbol})".format(name=x.name, symbol=x.symbol),
    )

    delete_unit_modifier = SubmitField("Delete Unit Modifier")


class UnitCombinationForm(FlaskForm):
    base_unit = QuerySelectField(
        "Base Unit",
        allow_blank=False,
        query_factory=get_current_base_units,
        get_label=lambda x: "{name} ({symbol})".format(name=x.name, symbol=x.symbol),
    )
    unit_modifier = QuerySelectField(
        "Unit Modifier",
        allow_blank=False,
        query_factory=get_current_unit_modifiers,
        get_label=lambda x: "{name} ({symbol})".format(name=x.name, symbol=x.symbol),
    )

    exponent = IntegerField("Exponent", validators=[InputRequired()])


class AddUnitForm(FlaskForm):
    unit_name = StringField("Unit Name", validators=[InputRequired()])
    unit_combinations = FieldList(FormField(UnitCombinationForm), min_entries=1)
    add_unit_part = SubmitField("Add Combination")
    add_unit = SubmitField("Add Unit")
