import logging
from pathlib import Path

from flask import Blueprint, render_template

from service.repos import files, index

logger = logging.getLogger(__name__)

view = Blueprint('files', __name__)


@view.get('/')
def files_list():
    files = index.getfiles()
    file_list = [file.dict() for file in files]
    logger.debug(file_list)
    return render_template(
        'files.html',
        file_list=file_list,
    )


@view.get('/card')
def file_card():
    file = Path('service/data/import/ОС.xlsx')
    file_data = files.internal_data(file)
    return render_template(
        'file_card.html',
        columns=file_data.columns,
        data=file_data.data,
    )
