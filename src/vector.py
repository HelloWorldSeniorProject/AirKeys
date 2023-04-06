# vector: a 4d vector with x, y, z for the position of a fingertip
# and time for the timestamp
class vector:
    def __init__(self, x, y, z, time):
        self.x = x
        self.y = y
        self.z = z
        self.time = time

# pos: a position of a 2d point on y=0 plane
class pos:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        
    def __str__(self):
        return f"({self.x}, {self.z})"

class layout:
    def __init__(self):
        self.keys = dict()
        
    def __str__(self):
        out = ""
        for x in self.keys:
            out += f"{x}: ({self.keys[x][0]}, {self.keys[x][1]}), \n"
        return out[:-3]
        
    # Adds a tuple of 2 positions into self.keys.
    # This tuple represents the endpoints of a 2d bounding box on y=0 plane,
    # where the first one is the top-left point,
    # and the second one is the bottom-right one.
    def add(self, value, pos1, pos2):
        self.keys[value] = pos1, pos2

# Simple Test
qwerty = layout()
qwerty.add('q', pos(0, 0), pos(1, 1))
qwerty.add('w', pos(1, 0), pos(2, 1))
qwerty.add('e', pos(2, 0), pos(3, 1))
print(qwerty)