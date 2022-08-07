import logging

import pandas as pd

from service import config, schemas

logger = logging.getLogger(__name__)
app_config = config.load_from_env()

import_dir = app_config.path.upload_dir


def internal_data(filename: str) -> schemas.FileData:
    excel_file = import_dir / f'{filename}.xlsx'
    fonds_frame = pd.read_excel(excel_file)
    return schemas.FileData(
        columns=list(fonds_frame.columns),
        data=fonds_frame.to_dict('records'),
    )
