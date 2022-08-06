import logging
import datetime
from pathlib import Path

from service import config
from service.schemas import ImportFiles

logger = logging.getLogger(__name__)

app_config = config.load_from_env()
import_dir = app_config.path.upload_dir


def getfiles() -> list[ImportFiles]:
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
