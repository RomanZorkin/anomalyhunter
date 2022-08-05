from flask import Blueprint, render_template

from service.forms.upload import FileForm

view = Blueprint('index', __name__)


@view.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm(meta={'csrf': False})
    title = 'Поиск аномалий'
    return render_template(
        'index.html',
        page_title=title,
        form=form,
    )
