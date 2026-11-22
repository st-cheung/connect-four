"""Data structures for communicating state between the controller and UI."""

from dataclasses import dataclass
from connect_four.enums import MessageType, TextType, Screen
from connect_four.board import ConnectFour


@dataclass
class MessageData:
    """Stores information about a message displayed by the UI."""

    type: MessageType
    success: bool
    until: int = 0


@dataclass
class UIState:
    """Stores the current state information needed by the UI."""

    screen: Screen
    game: ConnectFour | None
    game_result: TextType | None
    message: MessageData | None
