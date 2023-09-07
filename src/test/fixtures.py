import pytest
import logging
from swte import *


@pytest.fixture(autouse=True, scope="session")
def logger():
    format_str = "%(levelname)s [%(asctime)s]: %(message)s "
    formatter = logging.Formatter(format_str)

    # create logger
    logger = logging.getLogger("test")
    logger.setLevel(logging.DEBUG)

    # create and configure handlers.
    handlers = [logging.StreamHandler(), logging.FileHandler(LOG_FILE, "w")]
    for h in handlers:
        h.setLevel(logging.DEBUG)
        h.setFormatter(formatter)
        logger.addHandler(h)

    yield logger
    
# make a small space after test name for readability.
@pytest.fixture(autouse=True, scope="function")
def make_space():
    print("\n")
