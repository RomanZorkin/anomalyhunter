import logging

from service import config
from service.hunter import anomaly, weights
from service.schemas import FileSettings

logger = logging.getLogger(__name__)

app_config = config.load_from_env()
import_dir = app_config.path.upload_dir

#sheet = 'TDSheet'
#compare_col = 'ОКОФ'
#precision = 0.5
ind = 'ind'
#asset_name = 'ОС'


def hunt(filename: str, suffix: str, tun: FileSettings) -> bool:
    excel_file = import_dir / f'{filename}{suffix}'
    logger.debug(excel_file)

    if not weights.create_weights(excel_file, tun.precision, ind, tun.base_column, tun.sheet):
        return False
    if not anomaly.get_anomaly(
        filename, suffix, tun.sheet, tun.compare_column, tun.precision, ind,
    ):
        return False

    return True
