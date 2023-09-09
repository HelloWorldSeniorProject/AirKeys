import threading
from enum import Enum
from common.types import *
from common.patterns.singleton import Singleton


thread_lock = threading.Lock()


class ConfigTable(metaclass=Singleton):

    """A shared configuration for use across the system.

    Configuration Table is a singleton class that contains information about the system's state
    and other important configuration information. Utilizes thread locks to prevent concurrent
    access while modifying/retrieving table information.
    """

    DEFAULTS = {
        "state": SystemState.Standby,
        "layout": "Qwerty",
        "connection": Connection.UsbA,
        "device": Device.Large,
        "os": OperatingSystem.Windows,
    }

    def __init__(self):
        """Initializes the instance and sets a default state."""
        self._state = self.DEFAULTS["state"]
        self._layout = self.DEFAULTS["layout"]
        self._connection = self.DEFAULTS["connection"]
        self._device = self.DEFAULTS["device"]
        self._os = self.DEFAULTS["os"]

    def __init(self, prev_config: dict):
        """Intializes the instance to a previous state.

        Args:
            prev_config: a dictionary containing the last saved state.
        """
        self._state = prev_config.get("state", self.DEFAULTS["state"])
        self._layout = prev_config.get("layout", self.DEFAULTS["layout"])
        self._connection = prev_config.get("connection", self.DEFAULTS["connection"])
        self._device = prev_config.get("device", self.DEFAULTS["device"])
        self._os = prev_config.get("os", self.DEFAULTS["os"])

    def set_state(self, state: SystemState):
        """Sets the system state.

        Args:
            state : the SystemState to set.
        """
        with thread_lock:
            self._state = state

    def get_state(self) -> SystemState:
        """Fetches the system state.

        Returns:
            The SystemState currently set.
        """
        with thread_lock:
            return self._state

    # TODO : implement function as system evolves
    def setKeyboard(self, keyboard):
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
            "state": self._state,
            "layout": self._layout,
            "connection": self._connection,
            "device": self._device,
            "os": self._os,
        }
        return config
