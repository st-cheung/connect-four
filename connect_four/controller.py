"""Controls game flow and coordinates interactions between game logic and UI."""

import sys
from random import choice
import pygame as pg
from connect_four.board import ConnectFour
from connect_four.ai import ConnectFourAI
from connect_four.ui import ConnectFourUI
import connect_four.save_load as save_load
from connect_four.enums import Screen, MessageType, Player, Action, TextType
from connect_four.models import MessageData, UIState


class GameController:
    """Manages game state, processes actions and coordinates the game."""

    def __init__(self):
        self.ai = ConnectFourAI()
        self.ui = ConnectFourUI()
        self.running = True
        self.screen = Screen.MAIN_MENU
        self.game = None
        self.ai_player = None
        self.game_result = None
        self.message = None

    def run(self) -> None:
        """Run the main game loop."""
        clock = pg.time.Clock()
        while self.running:
            actions = self.ui.handle_events(self.screen)

            for action in actions:
                self._handle_action(action)

            self._update()
            self._draw()
            self.ui.update_display()
            clock.tick(60)
        sys.exit()

    def _start_game(self, game_mode: Action = Action.PLAY_HUMAN) -> None:
        self.game = ConnectFour()
        self.game_result = None
        self.screen = Screen.GAME
        self.ai_player = (
            choice((Player.ONE, Player.TWO)) if game_mode == Action.PLAY_AI else None
        )

    def _play_move(self, col: int) -> None:
        if self.game is None or self.game.is_terminal():
            return
        if not self.game.is_valid_move(col):
            return
        self.game.make_move(col)
        self._check_game_over()

    def _play_ai_move(self) -> None:
        assert self.game is not None
        col = self.ai.suggest_move(self.game)
        self._play_move(col)

    def _check_game_over(self) -> bool:
        assert self.game is not None
        if self.game.has_won(self.game.other_player_mask):
            self.game_result = (
                TextType.PLAYER1_WIN
                if self.game.current_player == Player.TWO
                else TextType.PLAYER2_WIN
            )
            self.screen = Screen.GAME_OVER
            return True
        if self.game.is_draw():
            self.game_result = TextType.DRAW
            self.screen = Screen.GAME_OVER
            return True
        return False

    def _save_game(self) -> None:
        if self.game is not None:
            if save_load.save_game(self.game, self.ai_player):
                self._show_message(MessageType.SAVE, True)
            else:
                self._show_message(MessageType.SAVE, False)

    def _load_game(self) -> None:
        game, self.ai_player = save_load.load_game()
        if game is None:
            self._show_message(MessageType.LOAD, False)
            return
        self.game = game
        self.game_result = None
        self._show_message(MessageType.LOAD, True)
        self.screen = Screen.GAME

    def _show_message(
        self, message_type: MessageType, success: bool, duration: int = 1000
    ) -> None:
        self.message = MessageData(
            type=message_type, success=success, until=pg.time.get_ticks() + duration
        )

    def _draw(self) -> None:
        state = UIState(
            screen=self.screen,
            game=self.game,
            game_result=self.game_result,
            message=self.message,
        )
        self.ui.draw(state)

    def _update(self) -> None:
        if self.game is None or self.game_result is not None:
            return
        if self.ai_player and self.game.current_player == self.ai_player:
            self._play_ai_move()
        if self.message and pg.time.get_ticks() >= self.message.until:
            self.message = None

    def _handle_action(self, action: Action | tuple[Action, int]) -> None:
        if isinstance(action, tuple):
            action, col = action
            self._play_move(col)
        else:
            if action == Action.QUIT:
                self.running = False
            if action == Action.PLAY_HUMAN:
                self._start_game()
            elif action == Action.PLAY_AI:
                assert action
                self._start_game(action)
            elif action == Action.RESUME_GAME:
                self.screen = Screen.GAME
            elif action == Action.SAVE_GAME:
                self._save_game()
                self.screen = Screen.GAME
            elif action == Action.LOAD_GAME:
                self._load_game()
            elif action == Action.RETURN_TO_MAIN_MENU:
                self.screen = Screen.MAIN_MENU
                self.game = None
            elif action == Action.PAUSE_GAME:
                self.screen = Screen.PAUSE
