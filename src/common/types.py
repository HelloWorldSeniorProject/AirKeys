from enum import Enum

""" Definitions of types and enums.
    
    Contains the type and enumeration definitions used within the system. Custom enumerations extend the Enum class 
    from the built-in enum module.
"""


class Mode(str, Enum):
    """An indicator of the system's current mode."""

    Standby = "Standby"
    Calibration = "Calibration"
    Inactive = "Inactive"
    Active = "Active"


class Device(str, Enum):
    Large = "Large"
    Small = "Small"


class Connection(str, Enum):
    """An indicator of the current method of connecting with a device."""

    UsbA = "UsbA"
    UsbC = "UsbC"
    Bluetooth = "Bluetooth"


class OperatingSystem(str, Enum):
    """An indicator of the current device's operating system."""

    Windows = "Windows"
    Linux = "Linux"
    Mac = "Mac"
    Android = "Android"
    IPhone = "iPhone"
