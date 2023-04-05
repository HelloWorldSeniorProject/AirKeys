
from common.types import *

class ConfigTable:
    
    __instance = None
    
    def __new__(cls):
        """Creates and/or returns singleton instance of ConfigTable.
        
        Returns:
            Shared instance of Config Table class.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        """Initializes the instance and sets a default state. 
        """
        self._state = SystemState.Standby
        self._keyboard = None
        self._connection = None
        self._device = None
        self._driver = None
        
    def ()