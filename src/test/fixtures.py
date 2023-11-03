import pytest
import logging
from swte import *
from common.patterns.singleton import Singleton

mapped_requirements = {}


@pytest.fixture(autouse=True, scope="session")
def logger():
    format_str = "%(levelname)-7s [%(asctime)s]: %(message)s"
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
def cleanup():
    print("\n")

    yield

    # pseudo-reset of env.
    Singleton._instances.clear()


@pytest.fixture(autouse=True, scope="session")
def map_requirements():
    # extract specified requirements as test runs.
    yield
    
    # empty line
    print("")
    compile_requirements_report()
    
    