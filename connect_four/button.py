"""Button rendering and interaction functionality."""

import pygame as pg
from connect_four.constants import (
    DEFAULT_TEXT_COLOUR,
    DEFAULT_BUTTON_COLOUR,
    BUTTON_HOVER_COLOUR,
    TEXTBOX_CORNER_RADIUS,
    DEFAULT_MARGINS,
)


class Button:
    """Represents an interactive UI button with hover behaviour."""

    def __init__(
        self,
        text: str,
        font: pg.Font,
        position: tuple[int, int],
        alignment: str = "center",
        margins: tuple[int, int] = DEFAULT_MARGINS,
        text_colour: pg.typing.ColorLike = DEFAULT_TEXT_COLOUR,
        button_colour: pg.typing.ColorLike = DEFAULT_BUTTON_COLOUR,
    ) -> None:
        self.text = text
        self.font = font
        self.text_colour = text_colour
        self.button_colour = button_colour
        self.margins = margins
        self.normal_surface = self._create_text_box(button_colour)
        self.hover_surface = self._create_text_box(BUTTON_HOVER_COLOUR)
        self.rect = self.normal_surface.get_rect(center=position)
        setattr(self.rect, alignment, position)

    def draw(self, screen: pg.Surface) -> None:
        """Draw the button onto the given surface"""
        surface = self.hover_surface if self.is_hovered() else self.normal_surface
        screen.blit(surface, self.rect)

    def is_hovered(self) -> bool:
        """Return if the button is hovered"""
        return self.rect.collidepoint(pg.mouse.get_pos())

    def _create_text_box(self, button_colour: pg.typing.ColorLike) -> pg.Surface:
        text = self.font.render(
            self.text, True, self.text_colour, bgcolor=button_colour
        )
        surface = pg.Surface(text.get_rect().inflate(*self.margins).size, pg.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        pg.draw.rect(
            surface,
            button_colour,
            surface.get_rect(),
            border_radius=TEXTBOX_CORNER_RADIUS,
        )

        text_rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, text_rect)
        return surface
