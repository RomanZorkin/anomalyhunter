import datetime
import logging
from pathlib import Path

import yaml

from service import config
from service.schemas import ImportFiles

logger = logging.getLogger(__name__)

app_config = config.load_from_env()
import_dir = app_config.path.upload_dir
utility_dir = app_config.path.utility_dir


def get_files() -> list[ImportFiles]:
    files = sorted(Path(import_dir).glob('*.xlsx'))
    logger.debug(files)
    import_files = []
    for file in files:
        import_files.append(ImportFiles(
            name=file.stem,
            suffix=file.suffix,
            date=datetime.datetime.fromtimestamp(file.stat().st_ctime, tz=datetime.timezone.utc),
        ))
    return import_files


def yaml_create(filename: str) -> bool:
    data = [{'filename': f'{filename}'}]
    yaml_file = utility_dir / f'{filename}.yaml'

    with open(yaml_file, 'w') as file:
        yaml.dump(data, file)
    return True
