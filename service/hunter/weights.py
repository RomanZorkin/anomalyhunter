import logging

logger = logging.getLogger(__name__)


def get_weights(filename: str, suffix: str) -> bool:
    logger.debug(f'{filename}{suffix}')
    return True
