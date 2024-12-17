from flask_wtf import FlaskForm
from wtforms import SubmitField


class MethodForm(FlaskForm):
    add_method = SubmitField("Add Method")
    edit_method = SubmitField("Edit Method")
    delete_method = SubmitField("Delete Method")
