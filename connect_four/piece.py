"""Rendering functionality for the current player's piece."""

import pygame as pg
from connect_four.constants import BLOCK_SIZE, PIECE_RADIUS, BACKGROUND_COLOUR


class Piece:
    """Represents the current player's piece displayed above the game board."""

    def __init__(
        self,
        color: pg.typing.ColorLike,
        radius: float = PIECE_RADIUS,
        background: pg.typing.ColorLike = BACKGROUND_COLOUR,
    ) -> None:
        self.colour = color
        self.radius = radius
        self.image = pg.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(background)
        pg.draw.circle(self.image, color, (0.5 * BLOCK_SIZE, 0.5 * BLOCK_SIZE), radius)
        self.rect = self.image.get_rect()

    def draw(self, screen: pg.Surface, pos: tuple[int, int]) -> None:
        """Draw the piece at the given position onto the surface"""
        screen.blit(self.image, pos)
