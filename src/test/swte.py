""" Provides a series of useful functions for use within the Software Test Environment.
"""
divider = "- "*50

def large_banner(string: str) :
    """Prints a string in a divider seperated format with extra whitespace. 
    
    Args:
        string: a string containing the desired text.    
    """
    print(f"\n{divider} \n\n{string}\n\n{divider}")

def small_banner(string: str) :
    """Prints a string in a divider seperated format without extra whitespace.
    
    Args:
        string: a string containing the desired text.    
    """
    print(f"\n\t- {string}")
    