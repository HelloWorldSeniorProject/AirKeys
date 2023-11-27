class Vector:
    """ A 4-component vector containing a fingertip position.

    Long description... Include any pertinent details like imports (ex. numpy), class methods,
    class variables, and major instance methods.
    """

    def __init__(self, x: float, y: float, z: float):
        """ Initializes the object based on passed x, y, z coordinates.
        
        Args:
            x : an integer representing the x coordinate of the finger.
            y : an integer representing the y coordinate of the finger.
            z : an integer representing the z coordinate of the finger.
        """
        self._x = x
        self._y = y
        self._z = z