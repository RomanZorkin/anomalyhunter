from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename


class FileForm(FlaskForm):
    file = FileField()

    def upload_file(self) -> bool:

        file = self.file.data
        filename = secure_filename(file.filename)
        files = {'file': (filename, file)}


        return True