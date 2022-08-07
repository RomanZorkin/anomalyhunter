import logging
from pathlib import Path

from flask import Blueprint, render_template, request

from service import config
from service.repos import files, index

logger = logging.getLogger(__name__)

view = Blueprint('files', __name__)


@view.get('/')
def files_list():
    data_files = index.getfiles()
    file_list = [file.dict() for file in data_files]
    logger.debug(file_list)
    return render_template(
        'files.html',
        file_list=file_list,
    )


@view.get('/card')
def file_card():
    filename = request.args.get('filename')
    file_data = files.internal_data(filename)
    return render_template(
        'file_card.html',
        columns=file_data.columns,
        data=file_data.data,
    )
