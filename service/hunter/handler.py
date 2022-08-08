import logging

from service import config
from service.hunter import anomaly, weights

logger = logging.getLogger(__name__)

app_config = config.load_from_env()
import_dir = app_config.path.upload_dir

sheet = 'Sheet1'
compare_col = 'срок службы'
precision = 0.5
ind = 'ind'
asset_name = 'ОС'


def hunt(filename: str, suffix: str) -> bool:
    excel_file = import_dir / f'{filename}{suffix}'
    logger.debug(excel_file)

    if not weights.create_weights(excel_file, precision, ind, asset_name):
        return False
    if not anomaly.get_anomaly(filename, suffix, sheet, compare_col, precision, ind):
        return False

    return True
