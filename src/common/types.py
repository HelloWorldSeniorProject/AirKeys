from enum import Enum

""" Definitions of types and enums.
    
    Contains the type and enumeration definitions used within the system. Custom enumerations extend the Enum class 
    from the built-in enum module.
"""


class Mode(Enum):
    """An indicator of the system's current mode."""

    Standby = 0
    Inactive = 1
    Active = 2


class Device(Enum):
    Large = 0
    Small = 1


class Connection(Enum):
    """An indicator of the current method of connecting with a device."""

    UsbA = 0
    UsbC = 1
    Bluetooth = 2


class OperatingSystem(Enum):
    """An indicator of the current device's operating system."""

    Windows = 0
    Linux = 1
    Mac = 2
    Android = 3
    IPhone = 4
