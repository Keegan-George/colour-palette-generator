from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import InputRequired


class FileUploadForm(FlaskForm):
    file = FileField(label="Choose image", validators=[InputRequired()])
    submit = SubmitField(label="Submit")
