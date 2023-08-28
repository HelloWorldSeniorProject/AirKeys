
from common.types import *
from util.singleton import Singleton
import threading

thread_lock = threading.Lock()

class ConfigTable(metaclass=Singleton):
    
    """A shared configuration for use across the system.
    
    Configuration Table is a singleton class that contains information about the system's state
    and other important configuration information. Utilizes thread locks to prevent concurrent
    access while modifying/retrieving table information. 
    """
    
    def __init__(self):
        """Initializes the instance and sets a default state. 
        """
        self._state = SystemState.Standby
        
        # TODO : initialize config table as necessary.
        # self._keyboard = None
        # self._connection = None
        # self._device = None
        # self._driver = None
    
    def set_state(self, state: SystemState):
        """Sets the system state.
        
        Args:
            state : the SystemState to set.
        """
        with thread_lock:
            self._state = state
        
    def get_state(self) -> SystemState:
        """Fetches the system state.
        
        Return:
            The SystemState currently set.
        """
        with thread_lock:
            return self._state

    # TODO : implement function as system evolves
    # def setKeyboard(self, keyboard):
    #     pass
    
    # def getKeyboard(self):
    #     pass

    # def setConnection(self, connection):
    #     pass
    
    # def getConnection(self):
    #     pass

    # def setDevice(self, device):
    #     pass
    
    # def getDevice(self) : 
    #     pass
    
    # def setDriver(self, driver):
    #     pass
    
    # def getDriver(self) :
    #     pass
    
    