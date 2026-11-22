import pytest
import json
from connect_four.board import ConnectFour
from connect_four.save_load import save_game, load_game
from connect_four.enums import Player

# pylint: skip-file


def test_save_load_with_ai(tmp_path):
    game = ConnectFour()
    for i in range(6):
        game.make_move(i)

    ai_player = Player.ONE
    save_game(game, ai_player=ai_player, filename=tmp_path / "save.json")
    loaded_game, loaded_ai = load_game(tmp_path / "save.json")
    assert loaded_game is not None
    assert loaded_game.board_mask == game.board_mask
    assert loaded_game.current_player == game.current_player
    assert loaded_game.log == game.log
    assert loaded_ai == ai_player


def test_save_load_without_ai(tmp_path):
    game = ConnectFour()
    for i in range(6):
        game.make_move(i)

    ai_player = None
    save_game(game, ai_player=ai_player, filename=tmp_path / "save.json")
    loaded_game, loaded_ai = load_game(tmp_path / "save.json")
    assert loaded_game is not None
    assert loaded_game.board_mask == game.board_mask
    assert loaded_game.current_player == game.current_player
    assert loaded_game.log == game.log
    assert loaded_ai == ai_player


def test_save_game(tmp_path):
    game = ConnectFour()
    game.make_move(2)

    path = tmp_path / "save.json"
    save_game(game, Player.ONE, path)

    expected_log = game.log
    expected_ai_player = 1

    data = json.loads(path.read_text())

    assert isinstance(data, dict)
    assert data["log"] == expected_log
    assert data["ai_player"] == expected_ai_player


def test_load_invalid_json(tmp_path):
    save_path = tmp_path / "save.json"
    save_path.write_text("{invalid: json")
    assert load_game(save_path) == (None, None)

    # missing field
    data = {"ai_player": 0}
    save_path.write_text(json.dumps(data))
    assert load_game(save_path) == (None, None)

    # wrong value type
    data = {"log": "invalid value", "ai_player": 0}
    save_path.write_text(json.dumps(data))
    assert load_game(save_path) == (None, None)

    # invalid move
    data = {"log": [-1], "ai_player": 0}
    save_path.write_text(json.dumps(data))
    assert load_game(save_path) == (None, None)

    # illegal move
    data = {"log": [0] * 7, "ai_player": 0}
    save_path.write_text(json.dumps(data))
    assert load_game(save_path) == (None, None)

    # game ended
    data = {"log": [j for i in range(4) for j in (i, i)], "ai_player": 0}
    save_path.write_text(json.dumps(data))
    assert load_game(save_path) == (None, None)

    # missing file
    save_path = tmp_path / "missing.json"
    assert load_game(save_path) == (None, None)
