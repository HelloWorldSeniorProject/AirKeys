import logging
import inspect
import os
from util.info import ROOT_DIR, LOGS_DIR


class Formatter(logging.Formatter):
    """Defines common message format for files."""

    # no explicit constructor necessary.

    minimal_details = "%(levelname)s: %(message)s "
    full_details = "[%(asctime)s] %(levelname)s : %(message)s (%(name)s:%(lineno)s)"
    LEVEL_STYLES = {
        logging.DEBUG: minimal_details,
        logging.INFO: minimal_details,
        logging.WARNING: minimal_details,
        logging.ERROR: full_details,
        logging.CRITICAL: full_details,
    }

    def format(self, record):
        """Converts log record into customized format.

        Returns:
            A formatted string.
        """
        log_format = self.LEVEL_STYLES[record.levelno]
        return logging.Formatter(log_format).format(record)


def get_logger(output_file: str, name: str = None) -> logging.Logger:
    """Creates a log of application activity.

    Returns:
        A logger object that records information to both the specified file and standard output.
    Note:
        Output file should be a filename and will be stored in the logs directory. If there is file with a matching name,
        the logger will create one. If a file with that name already exists, it will be overwritten.
    """

    # make logs directory if needed.
    if not (os.path.exists(LOGS_DIR)):
        os.mkdir(LOGS_DIR)

    # generate logger object.
    name = name if name is not None else os.path.relpath(inspect.stack()[1].filename, ROOT_DIR)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # accept all messages globally.

    log_formatter = Formatter()

    # add handler for stdout. This handler will capture information and error messages.
    std_out_handler = logging.StreamHandler()
    std_out_handler.setLevel(logging.WARNING)  # ignore debug and info messages on this handler.
    std_out_handler.setFormatter(log_formatter)
    logger.addHandler(std_out_handler)

    # add handler for a specified file. This handler will capture all messages.
    output_file = os.path.join(LOGS_DIR, output_file)
    file_handler = logging.FileHandler(output_file, mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    return logger
