"""Enumeration types used throughout the game."""

from enum import Enum, auto


class Screen(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    PAUSE = auto()
    GAME_OVER = auto()


class MessageType(Enum):
    SAVE = auto()
    LOAD = auto()


class TextType(Enum):
    TITLE = auto()
    PLAYER1_WIN = auto()
    PLAYER2_WIN = auto()
    DRAW = auto()


class Player(Enum):
    ONE = auto()
    TWO = auto()


class Action(Enum):
    PLAY_HUMAN = auto()
    PLAY_AI = auto()
    RETURN_TO_MAIN_MENU = auto()
    PAUSE_GAME = auto()
    RESUME_GAME = auto()
    SAVE_GAME = auto()
    LOAD_GAME = auto()
    MAKE_MOVE = auto()
    QUIT = auto()


class FontType(Enum):
    TITLE = auto()
    MENU_BUTTON = auto()
    PAUSE_BUTTON = auto()
    RETURN_BUTTON = auto()
    MESSAGE = auto()
    GAME_RESULT = auto()
