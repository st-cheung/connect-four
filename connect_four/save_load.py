"""Functions for saving and loading game states."""

import json
from pathlib import Path
from connect_four.board import ConnectFour
from connect_four.enums import Player

PLAYER_FROM_SAVE = {
    0: None,
    1: Player.ONE,
    2: Player.TWO,
}
PLAYER_TO_SAVE = {v: k for k, v in PLAYER_FROM_SAVE.items()}

SAVE_FILE = Path(__file__).parent / "savegame.json"


def save_game(
    game: ConnectFour, ai_player: Player | None, filename: Path = SAVE_FILE
) -> bool:
    """Save the game state to a file"""
    data = {"log": game.log, "ai_player": PLAYER_TO_SAVE[ai_player]}
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
    except OSError:
        return False
    return True


def load_game(filename: Path = SAVE_FILE) -> tuple[ConnectFour | None, Player | None]:
    """Load the game state from a file"""
    data = {}
    try:
        with open(filename) as f:
            data = json.load(f)
        log = data["log"]
        ai_player = PLAYER_FROM_SAVE[data["ai_player"]]
        game = ConnectFour()
        for col in log:
            if not (isinstance(col, int) or (0 <= col <= 6)):
                raise ValueError("Invalid column in log")
            if not game.is_valid_move(col):
                raise ValueError("Illegal move in log")
            if game.is_terminal():
                raise ValueError("Game already ended in log")
            game.make_move(col)
        assert game.log == log, "Log mismatch after replaying moves"
        if game.has_won(game.other_player_mask) or game.is_draw():
            raise ValueError("Game already ended in log")
    except (OSError, KeyError, ValueError, TypeError):
        return None, None
    return game, ai_player
