from processing.position import Position

class Layout:
    """ A collection of alphanumerical symbols and their positions.
    
    Long description... Include any pertinent details like imports (ex. numpy), class methods,
    class variables, and major instance methods.
    """

    def __init__(self):
        """ Initializes the object and creates empty key set."""

        self._keys = dict()
        
    def __str__(self):
        """ Fetches object's keys and their positions.
        
        Returns:
            A formatted string containing all of the layout's keys and their positions.
        """
        out = ""
        for x in self._keys:
            out += f"{x}: ({self._keys[x][0]}, {self._keys[x][1]}), \n"
        return out[:-3]
    

    def add(self, value: str , pos1: Position, pos2: Position):
        """Adds a key value and its position into keys dictionary.
        
        Args: 
            value : a char representing the alphanumeric value to assign to as the key.
            pos1 : a Position object representing the 2d bounding box on the top-left, y=0 plane.
            pos2 : a Position object representing the 2d bounding box on the bottom-right, y=0 plane.

        """
        self._keys[value] = pos1, pos2