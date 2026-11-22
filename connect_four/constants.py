"""Constants used throughout the game."""

import pygame as pg
from connect_four.enums import Player


def _lighten_colour(colour: pg.typing.ColorLike, factor: float = 1.1) -> pg.Color:
    colour = pg.Color(colour)
    return pg.Color(
        int(min(colour.r * factor, 255)),
        int(min(colour.g * factor, 255)),
        int(min(colour.b * factor, 255)),
        colour.a,
    )


def _darken_colour(colour: pg.typing.ColorLike, factor: float = 0.8) -> pg.Color:
    colour = pg.Color(colour)
    return pg.Color(*(int(c * factor) for c in colour[:3]))


# Define colors
BLUE = "royalblue3"
RED = "red4"
YELLOW = "darkgoldenrod"
GREEN = "green4"
GREY = "grey80"
WHITE = "white"

BACKGROUND_COLOUR = GREY
DEFAULT_TEXT_COLOUR = WHITE
DEFAULT_BUTTON_COLOUR = BLUE
BOARD_COLOUR = _darken_colour(BLUE)
TITLE_COLOUR = BLUE
BUTTON_HOVER_COLOUR = _lighten_colour(DEFAULT_BUTTON_COLOUR)
MESSAGE_BACKGROUND = _darken_colour(BACKGROUND_COLOUR)

PLAYER_COLOURS = {Player.ONE: YELLOW, Player.TWO: RED, None: BLUE}
SUCCESS_COLOUR = _darken_colour(GREEN)
FAIL_COLOUR = _darken_colour(RED)
MESSAGE_COLOUR = {True: SUCCESS_COLOUR, False: FAIL_COLOUR}

# Define sizes
NUM_ROWS = 6
NUM_COLS = 7
MAX_MOVES = NUM_ROWS * NUM_COLS
BLOCK_SIZE = 100
MESSAGE_AREA_HEIGHT = 50
BOARD_WIDTH = NUM_COLS * BLOCK_SIZE
BOARD_HEIGHT = NUM_ROWS * BLOCK_SIZE
WIDTH = BOARD_WIDTH
HEIGHT = BOARD_HEIGHT + BLOCK_SIZE + MESSAGE_AREA_HEIGHT
PIECE_RADIUS = 0.4 * BLOCK_SIZE
TEXTBOX_CORNER_RADIUS = 5
BOARD_CORNER_RADIUS = 8
DEFAULT_MARGINS = (20, 10)

# Bitboard masks
# Each column uses 7 bits, with the top bit acting as a sentinel.
BITS_PER_COL = NUM_ROWS + 1
TOP_MASK = int(("1" + "0" * NUM_ROWS) * NUM_COLS, 2)
BOTTOM_MASK = TOP_MASK >> NUM_ROWS
CENTRE_COL = NUM_COLS // 2
COLUMN_MASK = int("1" * NUM_ROWS, 2)
CENTRE_MASK = COLUMN_MASK << (BITS_PER_COL * CENTRE_COL)
COL_MASKS = [COLUMN_MASK << BITS_PER_COL * col for col in range(NUM_COLS)]

# AI settings
ALPHA_BETA = True
DEPTH = 8
CENTRE_WEIGHT = 5
WIN_MOVE_WEIGHT = 100
OPP_WIN_MOVE_WEIGHT = -150
# Order columns from the centre outwards to prioritise stronger positions.
MOVE_ORDER = [3, 2, 4, 1, 5, 0, 6]
