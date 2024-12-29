from flask_wtf import FlaskForm
from wtforms import FieldList, FileField, FormField, StringField, SubmitField
from wtforms.validators import InputRequired


class MethodForm(FlaskForm):
    add_method = SubmitField("Add Method")
    edit_method = SubmitField("Edit Method")
    delete_method = SubmitField("Delete Method")


class AddMethodPartForm(FlaskForm):
    method_part_name = StringField("Method Part Name", validators=[InputRequired()])


class AddMethodForm(FlaskForm):
    method_name = StringField("Method Name", validators=[InputRequired()])
    method_parts = FieldList(FormField(AddMethodPartForm), min_entries=1)
    add_method_part = SubmitField("Add Method Part")
    remove_method_part = SubmitField("Remove Method Part")
    method_file = FileField("Method File")
    add_method = SubmitField("Add Method")
    reset = SubmitField("Reset")
