class Position:
    """ A 2d point on y=0 plane. 

    Long description... Include any pertinent details like imports (ex. numpy), class methods,
    class variables, and major instance methods.
    """
    
    def __init__(self, x: float, z: float):
        """ Initializes the object based on passed x and z coordinates.
        
        Args:
            x : an integer representing the x coordinate on a y=0 plane.
            z : an integer representing the z coordinate on a y=0 plane.
        """
        self._x = x
        self._z = z
        
    def __str__(self):
        """ Fetches object's positions.
        
        Returns:
            A formatted string containing the object's x and z positions.
        
        Note:
            Called by referencing object like so : "print(obj)"
        """
        return f"({self._x}, {self._z})"
