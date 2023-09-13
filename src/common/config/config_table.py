import threading
from util.logger import get_logger
from common.types import *
from common.patterns.singleton import Singleton


thread_lock = threading.Lock()
logger = get_logger("ConfigTable.log")


class ConfigTable(metaclass=Singleton):

    """A shared configuration for use across the system.

    Configuration Table is a singleton class that contains information about the system's state
    and other important configuration information. Utilizes thread locks to prevent concurrent
    access while modifying/retrieving table information.
    """

    _DEFAULTS = {
        "mode": Mode.Standby,
        "layout": "Qwerty",
        "connection": Connection.UsbA,
        "device": Device.Large,
        "os": OperatingSystem.Windows,
    }

    def __init__(self):
        """Initializes the instance and sets a default state."""

        logger.info("Initializing the Config Table to default state.")
        self.default()

    def default(self):
        """Sets all variables to their default state"""
        logger.info("Setting default Config Table state.")
        self._mode = self._DEFAULTS["mode"]
        self._layout = self._DEFAULTS["layout"]
        self._connection = self._DEFAULTS["connection"]
        self._device = self._DEFAULTS["device"]
        self._os = self._DEFAULTS["os"]

    def write(self, prev_config: dict) -> bool:
        """Sets all variables to last a previous state.

        Args:
            prev_config: a dictionary containing the last saved config table state.

        Returns:
            True if operation was successful, false otherwise.
        """
        with thread_lock:
            logger.info(f"Attempting to overwrite current config table:\n {vars(self)}")

            if type(prev_config) != dict:
                logger.error(f"Passed configuration is not of type dictionary. Aborting operation.")
                return False

            # retrieve values from previous config. Note any missing values.
            if not (mode := prev_config.get("mode"), None):
                mode = self._DEFAULTS["mode"]
                logger.warning(f"Did not find prev mode, setting default {mode}.")

            if not (layout := prev_config.get("layout"), None):
                layout = self._DEFAULTS["layout"]
                logger.warning(f"Did not find prev layout, setting default {layout}.")

            if not (connection := prev_config.get("connection"), None):
                connection = self._DEFAULTS["connection"]
                logger.warning(f"Did not find prev connection type, setting default {connection}.")

            if not (device := prev_config.get("device"), None):
                device = self._DEFAULTS["device"]
                logger.warning(f"Did not find prev device type, setting default {device}.")

            if not (os := prev_config.get("os"), None):
                os = self._DEFAULTS["os"]
                logger.warning(f"Did not find prev operating system, setting default {os}.")

            self._mode = mode
            self._layout = layout
            self._connection = connection
            self._device = device
            self._os = os

            logger.info(f"Write operation was a success. New table:\n {vars(self)}")
            return True

    def set_mode(self, mode: Mode):
        """Sets the system's mode.

        Args:
            mode : the system mode to set.
        """
        with thread_lock:
            self._mode = mode

    def get_mode(self) -> Mode:
        """Fetches the system's mode.

        Returns:
            The system mode currently set.
        """
        with thread_lock:
            return self._mode

    # TODO : implement function as system evolves
    def set_layout(self, layout):
        pass

    def getKeyboard(self):
        pass

    def setConnection(self, connection):
        pass

    def getConnection(self):
        pass

    def setDevice(self, device):
        pass

    def getDevice(self):
        pass

    def to_dictionary(self) -> dict:
        """Converts config table to dictionary.

        Returns:
            A dictionary containing the current values of the config table.
        """

        config = {
            "mode": self._mode,
            "layout": self._layout,
            "connection": self._connection,
            "device": self._device,
            "os": self._os,
        }
        return config
