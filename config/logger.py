import logging

from config.settings import LOG_LEVEL


def setup_logger():
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
