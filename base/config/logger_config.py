import logging
from logging.handlers import RotatingFileHandler


def get_logger():
    """
    Purpose:
        Configure and return a robust logger instance for the application "myforeignjob".

    Request:
        No parameters.

    Response:
        Returns a configured logging.Logger object with DEBUG level,
        using a rotating file handler that writes logs to 'app.log'.

    Implementation Details:
        - The logger is named "myforeignjob" to clearly identify the application source.
        - Previous handlers are cleared to avoid duplicate logs if the logger is re-instantiated.
        - Logs include timestamp, filename, logger name, function name, log level, and the message.
        - Uses RotatingFileHandler to manage log file size and avoid uncontrolled growth.
        - Log propagation is disabled to prevent double logging in complex applications.

    Company Name: Softvan PCT Ltd
    """
    logger = logging.getLogger("myforeignjob")

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
