from flask_wtf import FlaskForm
from flask_wtf.file import FileField


class FileForm(FlaskForm):
    file = FileField()
