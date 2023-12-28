from maze import Maze
from game_controller import GameController


def test_constructor():
    g = GameController(600, 400)
    m = Maze(600, 400, 150, 450,
             100, 300, g)
    assert m.LEFT_VERT == 150
    assert m.RIGHT_VERT == 450
    assert m.TOP_HORIZ == 100
    assert m.BOTTOM_HORIZ == 300
    assert m.WIDTH == 600
    assert m.HEIGHT == 400
    assert m.gc is g
    assert m.dots.dots_left() == ((m.dots.WIDTH//m.dots.SPACING + 1) * 2 +
                                  (m.dots.HEIGHT//m.dots.SPACING + 1) * 2)


def test_eat_dots():
    g = GameController(600, 400)
    m = Maze(600, 400, 150, 450,
             100, 300, g)
    TH = m.TOP_HORIZ
    BH = m.BOTTOM_HORIZ
    WIDTH = m.WIDTH
    SPACING = 75
    num_dots = m.dots.dots_left()
    len_botton_row = len(m.dots.bottom_row)

    m.eat_dots(SPACING, TH)
    assert m.dots.dots_left() == num_dots - 1
    for i in range(WIDTH//SPACING + 1):
        m.eat_dots(i * SPACING, BH)
        assert len(m.dots.bottom_row) == len_botton_row - (i + 1)
