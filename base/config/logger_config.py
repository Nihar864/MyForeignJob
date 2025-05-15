import logging
from logging.handlers import RotatingFileHandler


def get_logger():
    logger = logging.getLogger("MyForeignJob")

    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler("app.log")

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(name)s -  %(funcName)s - %(levelname)s - %(message)s\n"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

    return logger
