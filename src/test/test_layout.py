from common.layout import Layout
from processing.position import Position as Pos

# Simple Test
qwerty = Layout()
qwerty.add('q', Pos(0, 0), Pos(1, 1))
qwerty.add('w', Pos(1, 0), Pos(2, 1))
qwerty.add('e', Pos(2, 0), Pos(3, 1))
print(qwerty)