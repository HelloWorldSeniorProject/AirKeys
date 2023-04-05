from enum import Enum

""" Definitions of types and enums.
    
    Contains the type and enumeration definitions used within the system. Custom enumerations extend the Enum class 
    from the built-in enum module.

"""

class SystemState(Enum):
    Standby = 0
    Inactive = 1
    Active = 2
    