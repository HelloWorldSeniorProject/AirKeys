import subprocess
from common.patterns.singleton import Singleton
from common.util.logger import get_logger

logger = get_logger()


class PowerInterface(metaclass=Singleton):
    def __init__(self):
        pass
