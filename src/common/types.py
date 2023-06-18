import enum

""" Definitions of types and enums.
    
    Contains the type and enumeration definitions used within the system. Custom enumerations extend the Enum class 
    from the built-in enum module.
"""


class SystemState(enum.Enum):
    """A description of the System's Current State."""

    #: System is not yet ready for use.
    Standby = 0

    #: System has not been used for system_timeout time limit. Ready to
    #: reconnect once active signal detected.
    Inactive = 1

    #: System is ready to use.
    Active = 2
