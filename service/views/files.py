import logging

from flask import Blueprint, redirect, render_template, request, url_for

from service.repos import files

logger = logging.getLogger(__name__)

view = Blueprint('files', __name__)


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
        file={'name': filename, 'suffix': suffix},
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


@view.get('/settings')
def file_settings():
    filename = request.args.get('filename')
    suffix = request.args.get('suffix')
    sheet = request.args.get('sheet')

    if not (filename and suffix):
        return render_template('mistake.html')

    yaml_sheet = files.yaml_sheet(filename)

    if not (sheet or yaml_sheet):
        logger.debug(sheet)
        sheets = files.get_sheets(filename, suffix)
        logger.debug(sheets)
        return render_template(
            'file_sheets.html',
            sheets=sheets,
            file={'name': filename, 'suffix': suffix},
        )

    if not sheet:
        if not yaml_sheet:
            return render_template('mistake.html')
        sheet = yaml_sheet

    files.sheet_to_yaml(filename, sheet)
    file_data = files.short_data(filename, suffix, sheet)
    return render_template(
        'file_sheet.html',
        columns=file_data.columns,
        data=file_data.data,
        file={'name': filename, 'sheet': sheet},
    )
