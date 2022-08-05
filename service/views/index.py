from pathlib import Path

from flask import Blueprint, redirect, render_template, request, url_for

from service import config
from service.forms.upload import FileForm

app_config = config.load_from_env()
view = Blueprint('index', __name__)
upload_dir = Path(app_config.upload_dir)


@view.route('/', methods=['GET', 'POST'])
def index():
    title = 'Поиск аномалий'

    form = FileForm(meta={'csrf': False})
    if form.validate_on_submit():
        file = request.files['file']
        upload_file = upload_dir / str(file.filename)
        file.save(upload_file)
        return redirect(url_for('index.index'))

    return render_template(
        'index.html',
        page_title=title,
        form=form,
    )
