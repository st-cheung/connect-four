"""Message rendering functionality for the game interface."""

import pygame as pg
from connect_four.constants import (
    DEFAULT_TEXT_COLOUR,
    MESSAGE_BACKGROUND,
    TEXTBOX_CORNER_RADIUS,
    DEFAULT_MARGINS,
)


class Message:
    """Represents a UI message with its associated display properties."""

    def __init__(
        self,
        text: str,
        font: pg.Font,
        text_colour: pg.typing.ColorLike = DEFAULT_TEXT_COLOUR,
        margins: tuple[int, int] = DEFAULT_MARGINS,
    ) -> None:
        self.text = font.render(text, True, text_colour)
        self.rect = self.text.get_rect()
        self.surface = pg.Surface(self.rect.inflate(*margins).size, pg.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        pg.draw.rect(
            self.surface,
            MESSAGE_BACKGROUND,
            self.surface.get_rect(),
            border_radius=TEXTBOX_CORNER_RADIUS,
        )
        setattr(self.rect, "center", self.surface.get_rect().center)
        self.surface.blit(self.text, self.rect)

    def draw(self, screen: pg.Surface, position: tuple[int, int]) -> None:
        """Draw the message at the given position onto the surface"""
        self.rect.center = position
        screen.blit(self.surface, self.rect)
