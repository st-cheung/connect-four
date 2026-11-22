import pytest
from connect_four.board import ConnectFour
from connect_four.constants import NUM_COLS, BITS_PER_COL

# pylint: skip-file


@pytest.mark.parametrize("move", [0, 3, 6])
def test_make_move(move):
    game = ConnectFour()

    game.make_move(move)

    expected_board_mask = expected_bit(move, 0)
    expected_player_mask = 0

    assert game.player_mask == expected_player_mask
    assert game.board_mask == expected_board_mask
    assert game.player_mask & ~game.board_mask == 0

    assert len(game.log) == 1


def test_make_move_alternating_players():
    game = ConnectFour()
    game.make_move(0)
    game.make_move(0)
    game.make_move(6)

    expected_player_mask = expected_bit(0, 1)
    expected_board_mask = expected_bit(0, 0) | expected_bit(0, 1) | expected_bit(6, 0)
    assert game.player_mask == expected_player_mask
    assert game.board_mask == expected_board_mask
    assert game.player_mask & ~game.board_mask == 0
    assert len(game.log) == 3


def test_make_move_fill_column():
    game = ConnectFour()
    fill_column(game, 6)

    expected_board_mask = sum(expected_bit(6, i) for i in range(6))
    expected_player_mask = expected_bit(6, 0) | expected_bit(6, 2) | expected_bit(6, 4)

    assert game.player_mask == expected_player_mask
    assert game.board_mask == expected_board_mask
    assert game.player_mask & ~game.board_mask == 0
    assert len(game.log) == 6


@pytest.mark.parametrize("move", [-1, 7, 100])
def test_make_move_invalid_column(move):
    game = ConnectFour()

    with pytest.raises(ValueError):
        game.make_move(move)


def test_unmove():
    game = ConnectFour()

    original_player_mask = game.player_mask
    original_board_mask = game.board_mask
    original_current_player = game.current_player
    original_log = game.log

    game.make_move(3)
    game.unmove()

    assert game.player_mask == original_player_mask
    assert game.board_mask == original_board_mask
    assert game.current_player == original_current_player
    assert game.log == original_log


def test_unmove_alternating_players():
    game = ConnectFour()

    original_player_mask = game.player_mask
    original_board_mask = game.board_mask
    original_current_player = game.current_player
    original_log = game.log

    game.make_move(3)
    game.make_move(3)
    game.make_move(4)
    game.unmove()
    game.unmove()
    game.unmove()

    assert game.player_mask == original_player_mask
    assert game.board_mask == original_board_mask
    assert game.current_player == original_current_player
    assert game.log == original_log


def test_unmove_empty_log():
    game = ConnectFour()
    with pytest.raises(ValueError):
        game.unmove()


def test_valid_move():
    game = ConnectFour()

    assert game.is_valid_move(0)
    assert game.is_valid_move(3)
    assert game.is_valid_move(6)


def test_valid_move_full_column():
    game = ConnectFour()

    for _ in range(6):
        game.make_move(0)

    assert not game.is_valid_move(0)


def test_valid_move_negative_index():
    game = ConnectFour()

    with pytest.raises(ValueError):
        game.make_move(-1)


def test_valid_move_out_of_range():
    game = ConnectFour()

    with pytest.raises(ValueError):
        game.make_move(NUM_COLS)


@pytest.mark.parametrize(
    "moves",
    [
        pytest.param([0, 0, 1, 1, 2, 2, 3], id="horizontal"),
        pytest.param([0, 1, 0, 1, 0, 1, 0], id="vertical"),
        pytest.param([0, 1, 1, 2, 2, 3, 2, 3, 3, 4, 3], id="diagonal up"),
        pytest.param([3, 2, 2, 1, 1, 0, 1, 0, 0, 4, 0], id="diagonal down"),
    ],
)
def test_has_won_with_winner(moves):
    game = ConnectFour()
    for col in moves:
        game.make_move(col)

    assert game.has_won(game.other_player_mask)


@pytest.mark.parametrize(
    "moves",
    [
        pytest.param([0, 1, 0, 1, 0, 1], id="three in a row"),
        pytest.param([0, 0, 1, 1, 2, 2, 4, 4], id="four in a row with gap"),
        pytest.param([0, 1, 3, 2], id="four pieces but not the same player"),
    ],
)
def test_has_won_no_winner(moves):
    game = ConnectFour()

    for col in moves:
        game.make_move(col)

    assert not game.has_won(game.other_player_mask)


def test_is_draw():
    game = ConnectFour()
    game.log = [0] * 41
    assert not game.is_draw()

    game.log = [0] * 42
    assert game.is_draw()


def test_legal_moves():
    game = ConnectFour()
    assert game.get_legal_moves() == [0, 1, 2, 3, 4, 5, 6]
    for i in range(7):
        fill_column(game, i)
    assert game.get_legal_moves() == []
    game.unmove()
    assert game.get_legal_moves() == [6]



def expected_bit(column, row):
    return 1 << (column * (BITS_PER_COL) + row)


def fill_column(game, column):
    for i in range(6):
        game.make_move(column)
