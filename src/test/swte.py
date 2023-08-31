# Provides a series of useful functions for use within the Software Test Environment.

import os, logging
from textwrap import wrap

# Globals
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
LOG_FILE = os.path.join(TEMP_DIR, "test_logs.log")

logger = logging.getLogger(__name__)
max_line_length = 70
divider = "-" * max_line_length


def truncate_str(string: str) -> list[str]:
    """Returns an array of strings truncated to an approximate size.

    Args:
        string: a string to be wrapped.
    """
    return wrap(string, max_line_length, break_long_words=False, break_on_hyphens=False)


def large_banner(string: str):
    """Prints a string in a divider seperated format with extra whitespace.

    Args:
        string: a string containing the desired text.
    """
    msg = truncate_str(string)

    # beginning space
    logger.info(f"{divider}")
    logger.info(f"")

    for s in msg:
        logger.info(f"- {s}")

    # end space
    logger.info(f"")
    logger.info(f"{divider}")


def small_banner(string: str):
    """Prints a string in a divider seperated format without extra whitespace.

    Args:
        string: a string containing the desired text.
    """
    msg = truncate_str(string)
    for s in msg:
        logger.info(f"{s}")
