import pytest
from connect_four.board import ConnectFour
from connect_four.ai import ConnectFourAI


# pylint: skip-file
def test_immediate_win():
    game = ConnectFour()
    ai = ConnectFourAI()
    moves = [0, 0, 1, 1, 2, 2]
    for i in moves:
        game.make_move(i)
    move = ai.suggest_move(game)
    assert move == 3


def test_immediate_block():
    game = ConnectFour()
    ai = ConnectFourAI()
    moves = [0, 0, 1, 1, 2]
    for i in moves:
        game.make_move(i)
    move = ai.suggest_move(game)
    assert move == 3


def test_returns_legal_move():
    game = ConnectFour()
    ai = ConnectFourAI()
    moves = [2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 1, 1, 1, 1, 1, 1, 5, 6, 5, 6]
    for i in moves:
        game.make_move(i)
    move = ai.suggest_move(game)
    assert move in game.get_legal_moves()


def test_ai_preserves_board_state():
    game = ConnectFour()
    ai = ConnectFourAI()
    moves = [2, 3, 3, 2, 2]
    for i in moves:
        game.make_move(i)
    move = ai.suggest_move(game)
    assert game.log == moves
