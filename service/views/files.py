import logging

from flask import Blueprint, redirect, render_template, request, url_for

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
    suffix = request.args.get('suffix')

    if not (filename and suffix):
        return render_template('mistake.html')

    file_data = files.internal_data(filename, suffix)
    return render_template(
        'file_card.html',
        columns=file_data.columns,
        data=file_data.data,
    )


@view.get('/hunter')
def anomaly_hunter():
    filename = request.args.get('filename')
    suffix = request.args.get('suffix')

    if not (filename and suffix):
        return render_template('mistake.html')

    if not files.find_anomaly(filename, suffix):
        return render_template('mistake.html')

    return redirect(url_for('index.index'))
