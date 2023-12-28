from dots import Dots


def test_constructor():
    ds = Dots(600, 600, 150, 450, 150, 450)
    assert ds.WIDTH == 600
    assert ds.HEIGHT == 600
    assert ds.TH == 150
    assert ds.BH == 450
    assert ds.LV == 150
    assert ds.RV == 450
    assert len(ds.bottom_row) == len(ds.top_row) == ds.WIDTH//ds.SPACING + 1
    assert len(ds.left_col) == len(ds.right_col) == ds.HEIGHT//ds.SPACING + 1
    for i in range(len(ds.left_col)):
        assert ds.left_col[i].x == ds.LV
        assert ds.left_col[i].y == ds.SPACING * i
    for i in range(len(ds.right_col)):
        assert ds.right_col[i].x == ds.RV
        assert ds.right_col[i].y == ds.SPACING * i
    for i in range(len(ds.top_row)):
        assert ds.top_row[i].x == ds.SPACING * i
        assert ds.top_row[i].y == ds.TH
    for i in range(len(ds.bottom_row)):
        assert ds.bottom_row[i].x == ds.SPACING * i
        assert ds.bottom_row[i].y == ds.BH


def test_eat():
    ds = Dots(600, 600, 150, 450, 150, 450)
    SPACING = ds.SPACING
    WIDTH = ds.WIDTH
    HEIGHT = ds.HEIGHT
    TH, BH, LV, RV = ds.TH, ds.BH, ds.LV, ds.RV
    num_dots = ds.dots_left()

    de = ds.eat(SPACING, TH)
    assert ds.dots_left() == num_dots - 1

    ds = Dots(600, 600, 150, 450, 150, 450)
    len_top_row = len(ds.top_row)
    for i in range(WIDTH//SPACING + 1):
        ds.eat(i * SPACING, TH)
        assert len(ds.top_row) == len_top_row - (i + 1)
    assert ds.dots_left() == num_dots - (i + 3)
    for i in range(WIDTH//SPACING + 1):
        ds.eat(i * SPACING, BH)
    for i in range(HEIGHT//SPACING + 1):
        ds.eat(LV, i * SPACING)
    for i in range(HEIGHT//SPACING + 1):
        ds.eat(RV, i * SPACING)
    assert ds.dots_left() == 0


def test_dots_left():
    ds = Dots(600, 600, 150, 450, 150, 450)
    dl = ds.dots_left()
    assert dl == ((ds.WIDTH//ds.SPACING + 1) * 2 +
                  (ds.HEIGHT//ds.SPACING + 1) * 2)
