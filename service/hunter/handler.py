import logging

from service import config
from service.hunter import anomaly, weights

logger = logging.getLogger(__name__)

app_config = config.load_from_env()
import_dir = app_config.path.upload_dir


def hunt(filename: str, suffix: str) -> bool:
    excel_file = import_dir / f'{filename}{suffix}'
    logger.debug(excel_file)
    if not weights.create_weights(excel_file):
        return False
    return True
