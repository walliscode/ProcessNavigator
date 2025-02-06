from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    DecimalField,
    FieldList,
    FormField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from process_navigator.extensions.database import db
from process_navigator.models.inputs import Input
from process_navigator.models.parameters import Param
from process_navigator.models.process import Entity, ProcessMethod
from process_navigator.models.process import Discipline


# group all queries here
def input_query():
    return db.session.execute(db.select(Input)).scalars()


def parameter_query():
    return db.session.execute(db.select(Param)).scalars()


def process_method_query():
    return db.session.execute(db.select(ProcessMethod)).scalars()


def discipline_query():
    return db.session.execute(db.select(Discipline)).scalars()


def entity_query():
    return db.session.execute(db.select(Entity)).scalars()


# starting from the smallest unit of the form and building up to the largets unit


class ValueForm(FlaskForm):
    value = DecimalField("Value", validators=[InputRequired()])


class InputsForm(FlaskForm):
    input = QuerySelectField("Input", query_factory=input_query, allow_blank=False)
    values = FieldList(FormField(ValueForm), min_entries=1)
    hold_input = SubmitField("Hold")


class ParametersForm(FlaskForm):
    parameter = QuerySelectField(
        "Parameter", query_factory=parameter_query, allow_blank=False
    )
    values = FieldList(FormField(ValueForm), min_entries=1)
    hold_parameter = SubmitField("Hold")


class ProcessStepForm(FlaskForm):
    # user select process method
    process_method = QuerySelectField(
        "Process Method", query_factory=process_method_query, allow_blank=False
    )
    select_method = SubmitField("Select Method")

    # this will cause a filter on the process method step whilst opening up inputs and parameters
    process_method_step = QuerySelectField("Process Method Step", allow_blank=False)
    inputs = FieldList(FormField(InputsForm), min_entries=0)
    add_input = SubmitField("Add Input")
    remove_input = SubmitField("Remove Input")
    parameters = FieldList(FormField(ParametersForm), min_entries=0)
    add_parameter = SubmitField("Add Parameter")
    remove_parameter = SubmitField("Remove Parameter")
    hold_process_step = SubmitField("Hold Process Step")


class ParentEntitiesForm(FlaskForm):
    parent_entity = QuerySelectField(
        "Parent Entity", query_factory=entity_query, allow_blank=False
    )
    hold_parent_entity = SubmitField("Hold Parent Entity")


class ProcessForm(FlaskForm):
    # user selects discipline and process date, these are unique to Process data as opposed to ProcessStep
    process_discipline = QuerySelectField(
        "Discipline", query_factory=discipline_query, allow_blank=False
    )
    process_date = DateField("Process Date", validators=[InputRequired()])

    process_steps = FieldList(FormField(ProcessStepForm), min_entries=1)
    add_process_step = SubmitField("Add Process Step")
    remove_process_step = SubmitField("Remove Process Step")
    hold_process_steps = SubmitField("Hold Process Steps")

    parent_entities = FieldList(FormField(ParentEntitiesForm), min_entries=0)
    add_parent_entity = SubmitField("Add Parent Entity")
    remove_parent_entity = SubmitField("Remove Parent Entity")
    hold_parent_entity = SubmitField("Hold Parent Entities")

    process_repeats = IntegerField("Process Repeats", validators=[InputRequired()])
    submit_process = SubmitField("Submit")


class ProcessPathForm(FlaskForm):
    # user builds up a process path by linking processes together
    start_path = SubmitField("Start Path")
    processes = FieldList(FormField(ProcessForm), min_entries=1)
    add_process = SubmitField("Add Process")
    remove_process = SubmitField("Remove Process")

    submit_path = SubmitField("Submit Path")
