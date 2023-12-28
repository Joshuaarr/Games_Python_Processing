from othello_fielld import OthelloField
from tile import Tile


def test_constructor():
    of = OthelloField(8, 100)
    assert of.FIELD_SIZE == 8
    assert of.CELL_SIZE == 100
    assert len(of.tile_table) == 8

    # See if the first 4 tiles place in right place
    assert of.tile_table[3][3].color == 255
    assert of.tile_table[4][4].color == 255
    assert of.tile_table[3][4].color == 0
    assert of.tile_table[4][3].color == 0
    # And the rest should be empty
    for i in range(8):
        for j in range(8):
            if not (i == 3 or i == 4
                    or j == 3 or j == 4):
                assert of.tile_table[i][j] == 0


def test_opp_curr_color():
    # See if it change the current color
    # to the opposite color
    of = OthelloField(8, 100)
    curr_color = of.curr_color
    of.opp_curr_color()
    if curr_color == 0:
        assert of.curr_color == 255
    else:
        assert of.curr_color == 0


def test_place_tile():
    # If it's placing tile properly
    of = OthelloField(8, 100)
    of.legal_list = [(5, 3)]
    assert of.place_tile(3, 3) is None
    assert of.place_tile(3, 4) is None
    of.curr_color = 255
    of.place_tile(5, 3)
    assert of.tile_table[5][3].color == 255
    of.place_tile(3, 5)
    assert of.tile_table[3][5] == 0
    of.legal_list = [(3, 5)]
    of.place_tile(3, 5)
    assert of.tile_table[3][5].color == 0


def test_place_black_tile():
    # If it's placing black tile properly
    of = OthelloField(8, 100)
    of.legal_list = [(5, 3)]
    assert of.place_black_tile(3, 3) is None

    of.curr_color == 255
    assert of.place_black_tile(5, 3) is None

    of.curr_color == 0
    of.place_black_tile(5, 3)
    assert of.tile_table[5][3].color == 0
    assert of.curr_color == 255


def test_is_in_field():
    # Judge if a axis given is in play field
    of = OthelloField(8, 100)
    x, y = -1, -1
    assert of.is_in_field(x, y) is False
    x, y = 9, 5
    assert of.is_in_field(x, y) is False
    x, y = 0, 0
    assert of.is_in_field(x, y) is True
    x, y = 5, 5
    assert of.is_in_field(x, y) is True


def test_search_one_more():
    of = OthelloField(8, 100)
    curr, opp = 0, 255
    x, y, i, j = 5, 3, -1, 0
    assert of.search_one_more(x, y, i, j, curr, opp) is True
    i, j = 1, 0
    assert of.search_one_more(x, y, i, j, curr, opp) is False

    of = OthelloField(4, 100)
    curr, opp = 0, 255
    x, y, i, j = 3, 1, -1, 0
    assert of.search_one_more(x, y, i, j, curr, opp) is True
    i, j = 1, 0
    assert of.search_one_more(x, y, i, j, curr, opp) is False

    # Not in field, return false
    of = OthelloField(2, 100)
    curr, opp = 0, 255
    x, y, i, j = 3, 1, -1, 0
    assert of.search_one_more(x, y, i, j, curr, opp) is False


def test_search_posi():
    # If it's creating a proper search_posi_list
    of = OthelloField(8, 100)
    curr, opp = 255, 0
    of.search_posi(4, 3, curr, opp)
    assert of.search_posi_list == [(3, 2), (4, 2), (5, 2), (5, 3), (5, 4)]


def test_search_empt_posi():
    # If it's creating a proper legal_list
    of = OthelloField(8, 100)
    curr, opp = 255, 0
    assert of.legal_list == []
    assert of.tile_table[4][3].color == opp
    of.search_posi_list = [(5, 3)]
    of.search_empt_posi(curr, opp)
    assert of.legal_list == [(5, 3)]


def test_create_legal_list():
    # If it's creating a proper legal list
    of = OthelloField(8, 100)
    assert of.legal_list == []
    of.create_legal_list()
    assert of.legal_list == [(2, 3), (3, 2), (4, 5), (5, 4)]
    # If it's creating a proper legal list after a legal move
    of.place_black_tile(2, 3)
    of.create_legal_list()
    assert of.legal_list == [(2, 2), (2, 4), (4, 2)]


def test_flip_tile():
    # Test if flipping tile properly
    of = OthelloField(8, 100)
    of.flip_tile(2, 3)
    assert of.tile_table[3][3].color == 0
    assert of.tile_table[4][4].color == 255


def test_num_flipped():
    # Test if counting flipped tiles correctly
    of = OthelloField(8, 100)
    assert of.num_flipped(2, 3) == 1
    of.create_legal_list()
    of.place_tile(2, 3)
    assert of.num_flipped(2, 4) == 1


def test_find_max_to_flip():
    # Test if it can find the maximum number of place to flip
    of = OthelloField(6, 100)

    # Initialize tile_table
    tile_table = of.tile_table
    for i in range(len(tile_table)):
        for j in range(len(tile_table)):
            tile_table[i][j] = 0
    for i in range(1, len(tile_table) - 1):
        tile_table[i][2] = Tile(i, 2, 0)
    tile_table[3][1] = Tile(3, 1, 255)
    tile_table[0][2] = Tile(0, 2, 255)
    of.curr_color = 255
    of.create_legal_list()
    assert of.find_max_to_flip() == (5, 2)
