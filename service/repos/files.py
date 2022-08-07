import logging
from pathlib import Path

import pandas as pd

from service import config, schemas

logger = logging.getLogger(__name__)
app_config = config.load_from_env()

import_dir = app_config.path.upload_dir
file = import_dir / 'ОС.xlsx'


def internal_data(excel_file: Path) -> schemas.FileData:
    fonds_frame = pd.read_excel(excel_file)
    return schemas.FileData(
        columns=list(fonds_frame.columns),
        data=fonds_frame.to_dict('records'),
    )
