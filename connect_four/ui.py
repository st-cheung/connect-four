"""Rendering and input handling for the game interface."""

import pygame as pg
from connect_four.message import Message
from connect_four.button import Button
from connect_four.piece import Piece
from connect_four.board import ConnectFour
from connect_four.enums import Screen, Player, Action, FontType, MessageType, TextType
from connect_four.models import UIState
from connect_four.constants import (
    BLOCK_SIZE,
    WIDTH,
    HEIGHT,
    BOARD_WIDTH,
    BOARD_HEIGHT,
    MESSAGE_AREA_HEIGHT,
    NUM_COLS,
    NUM_ROWS,
    BITS_PER_COL,
    PIECE_RADIUS,
    BOARD_CORNER_RADIUS,
    TITLE_COLOUR,
    BOARD_COLOUR,
    BACKGROUND_COLOUR,
    PLAYER_COLOURS,
    MESSAGE_COLOUR,
)


class ConnectFourUI:
    """Manages UI elements, renders screens and translates user input into actions."""

    def __init__(self):
        pg.init()
        self.surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.pause_overlay = pg.Surface((WIDTH, HEIGHT), flags=pg.SRCALPHA)
        self.pause_overlay.fill((0, 0, 0, 100))
        pg.display.set_caption("Connect 4")
        self.fonts = self._create_fonts()
        self.text = {
            TextType.TITLE: self._create_text(
                "Connect 4", FontType.TITLE, TITLE_COLOUR
            ),
            TextType.PLAYER1_WIN: self._create_text(
                "Player 1 Wins",
                FontType.GAME_RESULT,
                PLAYER_COLOURS[Player.ONE],
            ),
            TextType.PLAYER2_WIN: self._create_text(
                "Player 2 Wins",
                FontType.GAME_RESULT,
                PLAYER_COLOURS[Player.TWO],
            ),
            TextType.DRAW: self._create_text(
                "It's a draw", FontType.GAME_RESULT, PLAYER_COLOURS[None]
            ),
        }
        self.temp_messages = {
            (MessageType.SAVE, True): Message(
                "Game saved",
                self.fonts[FontType.MESSAGE],
                MESSAGE_COLOUR[True],
            ),
            (MessageType.SAVE, False): Message(
                "Save failed", self.fonts[FontType.MESSAGE], MESSAGE_COLOUR[False]
            ),
            (MessageType.LOAD, True): Message(
                "Game loaded", self.fonts[FontType.MESSAGE], MESSAGE_COLOUR[True]
            ),
            (MessageType.LOAD, False): Message(
                "Load failed", self.fonts[FontType.MESSAGE], MESSAGE_COLOUR[False]
            ),
        }
        self.buttons = self._create_buttons()
        self.cursor_piece = {
            Player.ONE: Piece(PLAYER_COLOURS[Player.ONE]),
            Player.TWO: Piece(PLAYER_COLOURS[Player.TWO]),
        }
        self.board = self._create_board()

    def handle_events(self, screen: Screen) -> list[Action | tuple[Action, int]]:
        """Translate user inputs into controller actions."""
        actions = []
        buttons = self.buttons[screen]

        for event in pg.event.get():
            if event.type == pg.QUIT:
                actions.append(Action.QUIT)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                action = self._handle_button_event(buttons)
                if action is not None:
                    actions.append(action)
                    continue
                if screen == Screen.GAME:
                    col = self._get_column(event.pos)
                    if col is not None:
                        actions.append((Action.MAKE_MOVE, col))
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if screen == Screen.GAME:
                        actions.append(Action.PAUSE_GAME)
                    elif screen == Screen.PAUSE:
                        actions.append(Action.RESUME_GAME)
        return actions

    def update_display(self) -> None:
        """Update the display"""
        pg.display.update()

    def draw(self, state: UIState) -> None:
        """Draw the current screen"""
        self._draw_background()
        if state.screen == Screen.MAIN_MENU:
            self._draw_main_menu()
        elif state.screen == Screen.GAME or state.screen == Screen.GAME_OVER:
            assert state.game is not None
            self._draw_game(state.game, state.game_result)
        elif state.screen == Screen.PAUSE:
            assert state.game is not None
            self._draw_pause_menu(state.game)
        if state.message and state.message.until > pg.time.get_ticks():
            key = (state.message.type, state.message.success)
            self.temp_messages[key].draw(
                self.surface, (WIDTH // 2, MESSAGE_AREA_HEIGHT // 2)
            )

    def _draw_background(self) -> None:
        self.surface.fill(BACKGROUND_COLOUR)

    def _create_text(
        self, text: str, font_type: FontType, text_colour: pg.typing.ColorLike
    ) -> pg.Surface:
        return self.fonts[font_type].render(text, True, text_colour)

    def _draw_cursor_piece(self, player: Player, mouse_x: int) -> None:
        piece = self.cursor_piece[player]
        x_pos = int(self._clamp(mouse_x, 0, WIDTH - BLOCK_SIZE))
        y_pos = MESSAGE_AREA_HEIGHT
        piece.draw(self.surface, (x_pos, y_pos))

    def _get_cell_position(self, row, col) -> tuple[int, int]:
        x = (col + 0.5) * BLOCK_SIZE
        y = HEIGHT - (row + 0.5) * BLOCK_SIZE
        return (x, y)

    def _draw_board(self, game: ConnectFour) -> None:
        player1_mask = game.player_mask
        player2_mask = game.other_player_mask
        if game.current_player == Player.TWO:
            player1_mask, player2_mask = player2_mask, player1_mask
        self.surface.blit(self.board, (0, BLOCK_SIZE + MESSAGE_AREA_HEIGHT))
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                pg.draw.circle(
                    self.surface,
                    BACKGROUND_COLOUR,
                    ((col + 0.5) * BLOCK_SIZE, HEIGHT - (row + 0.5) * BLOCK_SIZE),
                    PIECE_RADIUS,
                )
                if (1 << (row + BITS_PER_COL * col)) & player1_mask:
                    pg.draw.circle(
                        self.surface,
                        PLAYER_COLOURS[Player.ONE],
                        ((col + 0.5) * BLOCK_SIZE, HEIGHT - (row + 0.5) * BLOCK_SIZE),
                        PIECE_RADIUS,
                    )
                elif (1 << (row + BITS_PER_COL * col)) & player2_mask:
                    pg.draw.circle(
                        self.surface,
                        PLAYER_COLOURS[Player.TWO],
                        ((col + 0.5) * BLOCK_SIZE, HEIGHT - (row + 0.5) * BLOCK_SIZE),
                        PIECE_RADIUS,
                    )

    def _draw_main_menu(self) -> None:
        self._draw_text(self.text[TextType.TITLE], (WIDTH // 2, BLOCK_SIZE))
        for button in self.buttons[Screen.MAIN_MENU].values():
            button.draw(self.surface)

    def _draw_game(self, game: ConnectFour, game_result: TextType | None) -> None:
        self._draw_board(game)
        if game_result is not None:
            return_button = self.buttons[Screen.GAME_OVER][Action.RETURN_TO_MAIN_MENU]
            return_button.draw(self.surface)
            message_height = (
                WIDTH // 2,
                (
                    MESSAGE_AREA_HEIGHT
                    + BLOCK_SIZE
                    + self.buttons[Screen.GAME_OVER][
                        Action.RETURN_TO_MAIN_MENU
                    ].rect.bottom
                )
                // 2,
            )
            self._draw_text(self.text[game_result], message_height)
        else:
            mouse_x = pg.mouse.get_pos()[0]
            self._draw_cursor_piece(game.current_player, mouse_x)
            pause = self.buttons[Screen.GAME][Action.PAUSE_GAME]
            pause.draw(self.surface)

    def _draw_text(self, text_surface: pg.Surface, position: tuple[int, int]) -> None:
        rect = text_surface.get_rect(center=position)
        self.surface.blit(text_surface, rect)

    def _draw_pause_menu(self, game: ConnectFour) -> None:
        self._draw_game(game, None)
        self.surface.blit(self.pause_overlay, (0, 0))
        for button in self.buttons[Screen.PAUSE].values():
            button.draw(self.surface)

    def _handle_button_event(self, buttons: dict[Action, Button]) -> Action | None:
        for action in buttons:
            if buttons[action].is_hovered():
                return action
        return None

    def _get_column(self, mouse_pos: tuple[int, int]) -> int:
        return int(mouse_pos[0] // BLOCK_SIZE)

    def _create_buttons(self) -> dict[Screen, dict[Action, Button]]:
        return {
            Screen.MAIN_MENU: {
                action: Button(
                    text=text,
                    font=self.fonts[FontType.MENU_BUTTON],
                    position=(WIDTH // 2, BLOCK_SIZE * (2 + i)),
                )
                for i, (action, text) in enumerate(
                    [
                        (Action.PLAY_HUMAN, "Play vs a friend"),
                        (Action.PLAY_AI, "Play vs computer"),
                        (Action.LOAD_GAME, "Load Game"),
                        (Action.QUIT, "Quit"),
                    ]
                )
            },
            Screen.PAUSE: {
                action: Button(
                    text=text,
                    font=self.fonts[FontType.MENU_BUTTON],
                    position=(WIDTH // 2, BLOCK_SIZE * (2 + i)),
                )
                for i, (action, text) in enumerate(
                    [
                        (Action.RESUME_GAME, "Resume"),
                        (Action.SAVE_GAME, "Save Game"),
                        (Action.RETURN_TO_MAIN_MENU, "Main Menu"),
                        (Action.QUIT, "Quit"),
                    ]
                )
            },
            Screen.GAME: {
                Action.PAUSE_GAME: Button(
                    "ESC",
                    self.fonts[FontType.PAUSE_BUTTON],
                    (WIDTH, 0),
                    alignment="topright",
                    margins=(10, 20),
                ),
            },
            Screen.GAME_OVER: {
                Action.RETURN_TO_MAIN_MENU: Button(
                    "Main Menu",
                    self.fonts[FontType.RETURN_BUTTON],
                    (WIDTH // 2, MESSAGE_AREA_HEIGHT // 2),
                )
            },
        }

    def _create_fonts(self) -> dict[FontType, pg.Font]:
        return {
            FontType.TITLE: pg.font.SysFont("arialblack", 64),
            FontType.MENU_BUTTON: pg.font.SysFont("arialblack", 40),
            FontType.RETURN_BUTTON: pg.font.SysFont("arialblack", 24),
            FontType.PAUSE_BUTTON: pg.font.SysFont("arialblack", 24),
            FontType.MESSAGE: pg.font.SysFont("arialblack", 24),
            FontType.GAME_RESULT: pg.font.SysFont("arialblack", 32),
        }

    def _create_board(self) -> pg.Surface:
        surface = pg.Surface((BOARD_WIDTH, BOARD_HEIGHT), flags=pg.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        pg.draw.rect(
            surface, BOARD_COLOUR, surface.get_rect(), border_radius=BOARD_CORNER_RADIUS
        )
        return surface

    def _clamp(self, value: float, minimum: float, maximum: float) -> float:
        return max(minimum, min(value, maximum))
