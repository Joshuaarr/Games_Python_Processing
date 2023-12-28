from tile import Tile


def test_constructor():
    tile = Tile(1, 2, 0)
    assert tile.color == 0
    assert tile.column == 1
    assert tile.row == 2
