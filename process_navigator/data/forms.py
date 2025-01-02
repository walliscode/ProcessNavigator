from flask_wtf import FlaskForm
from wtforms import FieldList, FileField, FormField, StringField, SubmitField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from process_navigator.extensions import db
from process_navigator.models.process import ProcessMethod


class MethodForm(FlaskForm):
    add_method = SubmitField("Add Method")
    edit_method = SubmitField("Edit Method")
    delete_method = SubmitField("Delete Method")


def get_current_process_methods():
    return db.session.execute(db.select(ProcessMethod)).scalars()


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
