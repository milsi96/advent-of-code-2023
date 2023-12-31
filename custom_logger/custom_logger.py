import logging
import sys


class CustomLogger:
    name: str

    def __init__(self, name: str):
        self.name = name

    def get_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(
            logging.Formatter(
                '[%(asctime)s] [%(levelname)s] '
                '[%(filename)s] [%(funcName)s] %(message)s'
            )
        )
        logger.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)

        return logger
