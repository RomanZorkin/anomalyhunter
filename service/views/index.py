from flask import Blueprint, redirect, render_template, request, url_for

from service import config
from service.repos import index as ind
from service.forms.upload import FileForm

app_config = config.load_from_env()
view = Blueprint('index', __name__)
upload_dir = app_config.path.upload_dir


@view.route('/', methods=['GET', 'POST'])
def index():
    title = 'Поиск аномалий'
    data_files = ind.get_files()
    file_list = [file.dict() for file in data_files]

    form = FileForm(meta={'csrf': False})
    if form.validate_on_submit():
        file = request.files['file']
        upload_file = upload_dir / str(file.filename)
        file.save(upload_file)
        ind.yaml_create(upload_file.stem)
        return redirect(url_for('index.index'))

    return render_template(
        'index.html',
        page_title=title,
        form=form,
        file_list=file_list,
    )
