import logging
from typing import Optional

import pandas as pd
import yaml

from service import config, schemas
from service.hunter import handler

logger = logging.getLogger(__name__)
app_config = config.load_from_env()

import_dir = app_config.path.upload_dir
utility_dir = app_config.path.utility_dir


def internal_data(filename: str, suffix: str) -> schemas.FileData:
    excel_file = import_dir / f'{filename}{suffix}'
    fonds_frame = pd.read_excel(excel_file)
    return schemas.FileData(
        columns=list(fonds_frame.columns),
        data=fonds_frame.to_dict('records'),
    )


def short_data(filename: str, suffix: str, sheet: str) -> schemas.FileData:
    excel_file = import_dir / f'{filename}{suffix}'
    fonds_frame = pd.read_excel(excel_file, sheet_name=sheet)
    return schemas.FileData(
        columns=list(fonds_frame.columns),
        data=fonds_frame.to_dict('records'),
    )


def find_anomaly(filename: str, suffix: str) -> bool:
    if not handler.hunt(filename, suffix):
        return False
    return True


def get_sheets(filename: str, suffix: str) -> list[str]:
    excel_file = import_dir / f'{filename}{suffix}'
    fonds_frame = pd.ExcelFile(excel_file)
    return list(fonds_frame.sheet_names)


def yaml_sheet(filename: str) -> Optional[str]:
    yaml_file = utility_dir / f'{filename}.yaml'

    with open(yaml_file) as file:
        settings = yaml.full_load(file)

    if not settings['sheet']:
        return False
    
    return settings['sheet']


def sheet_to_yaml(filename: str, sheet: str) -> None:
    yaml_file = utility_dir / f'{filename}.yaml'

    with open(yaml_file) as file:
        settings = yaml.full_load(file)

    settings['sheet'] = sheet
    with open(yaml_file, 'w') as file:
        yaml.dump(settings, file)
