from enum import Enum

""" Definitions of types and enums.
    
    Contains the type and enumeration definitions used within the system. Custom enumerations extend the Enum class 
    from the built-in enum module.
"""


class Mode(str, Enum):
    """An indicator of the system's current mode."""

    Standby = "Standby"
    Inactive = "Inactive"
    Active = "Active"


class Device(Enum):
    Large = "Large"
    Small = "Small"


class Connection(Enum):
    """An indicator of the current method of connecting with a device."""

    UsbA = "UsbA"
    UsbC = "UsbC"
    Bluetooth = "Bluetooth"


class OperatingSystem(Enum):
    """An indicator of the current device's operating system."""

    Windows = "Windows"
    Linux = "Linux"
    Mac = "Mac"
    Android = "Android"
    IPhone = "iPhone"
