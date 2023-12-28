FIELD_SIZE = 8
CELL_SIZE = 100


def setup():
    global field
    from othello_fielld import OthelloField
    size(FIELD_SIZE * CELL_SIZE, FIELD_SIZE * CELL_SIZE)
    field = OthelloField(FIELD_SIZE, CELL_SIZE)
    field.display()


def draw():
    field.display()


def mouseClicked():
    x = mouseX//CELL_SIZE
    y = mouseY//CELL_SIZE
    field.place_black_tile(x, y)
