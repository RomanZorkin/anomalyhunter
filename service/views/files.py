import logging

from flask import Blueprint, render_template

from service.repos import index

logger = logging.getLogger(__name__)

view = Blueprint('files', __name__)


@view.route('/', methods=['GET', 'POST'])
def files_list():
    files = index.getfiles()
    file_list = [file.dict() for file in files]
    logger.debug(file_list)
    return render_template(
        'files.html',
        file_list=file_list,
    )
