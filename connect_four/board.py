"""Connect Four game state and board logic."""

from connect_four.enums import Player
from connect_four.constants import (
    TOP_MASK,
    BOTTOM_MASK,
    COL_MASKS,
    MAX_MOVES,
    NUM_COLS,
    NUM_ROWS,
    BITS_PER_COL,
)


class ConnectFour:
    """Manages the Connect Four board state and game logic."""

    def __init__(
        self,
        board_mask: int = 0,
        player_mask: int = 0,
        current_player: Player = Player.ONE,
        log: list[int] | None = None,
    ):
        if log is None:
            log = []
        self.board_mask = board_mask
        self.player_mask = player_mask
        self.current_player = current_player
        self.log = [] if not log else log

    @property
    def other_player(self) -> Player:
        """Return the opposing player"""
        return Player.TWO if self.current_player == Player.ONE else Player.ONE

    @property
    def other_player_mask(self) -> int:
        """Return the opposing player mask"""
        return self.player_mask ^ self.board_mask

    @staticmethod
    def has_won(player_mask: int) -> bool:
        """Check whether the given player has won"""

        # Check horizontal, vertical and both diagonal directions.
        for d in (1, NUM_ROWS, 7, 8):
            # Check for 4 aligned pieces
            two = player_mask & (player_mask >> d)
            if two & (two >> 2 * d):
                return True
        return False

    def is_terminal(self) -> bool:
        """Check whether the game is over"""
        return self.has_won(self.other_player_mask) or self.is_draw()

    def is_draw(self) -> bool:
        """Check whether the game is a draw"""
        return len(self.log) >= MAX_MOVES

    def is_valid_move(self, col: int) -> bool:
        """Check whether the given move is valid"""

        if not 0 <= col < NUM_COLS:
            raise ValueError("Column index out of range")

        # Check whether the top cell in the column is occupied.
        return (self.board_mask & (1 << (BITS_PER_COL * col + NUM_ROWS - 1))) == 0

    def make_move(self, col: int) -> None:
        """Apply a move to the board state."""
        if not self.is_valid_move(col):
            raise ValueError("Invalid move")
        self.log.append(col)
        # Switch player perspective
        self.player_mask ^= self.board_mask
        self._switch_player()
        # Update the board occupancy mask.
        self.board_mask |= (1 << (BITS_PER_COL * col)) + self.board_mask

    def unmove(self) -> None:
        """Undo the last move"""

        if not self.log:
            raise ValueError("No moves to undo")
        col = self.log.pop()
        # Get the bit for the last played piece
        pos = (self.board_mask & COL_MASKS[col]).bit_length() - 1

        # Update the board occupancy mask.
        self.board_mask ^= 1 << pos

        # Switch player perspective
        self.player_mask ^= self.board_mask
        self._switch_player()

    def get_winning_mask(self, player_mask: int) -> int:
        """Return a mask of the immediate winning positions"""
        legal = self._get_possible_move_mask()
        wins = 0

        # Check  horizontal, vertical and both diagonal directions.
        for d in (1, BITS_PER_COL - 1, BITS_PER_COL, BITS_PER_COL + 1):
            x = player_mask & (player_mask >> d) & (player_mask >> 2 * d)
            # _xxx
            wins |= x >> d
            if d != 1:
                # xxx_
                wins |= x << 3 * d
                # x_xx
                x = player_mask & (player_mask >> d) & (player_mask >> 3 * d)
                wins |= x << 2 * d

                # xx_x
                x = player_mask & (player_mask >> 2 * d) & (player_mask >> 3 * d)
                wins |= x << d
        return wins & legal

    def get_legal_moves(self) -> list[int]:
        """Return the current legal moves"""
        return self._get_columns_from_mask(self._get_possible_move_mask())

    def get_winning_moves(self, player_mask: int) -> list[int]:
        """Return the immediate winning moves"""
        winning = self.get_winning_mask(player_mask)
        return self._get_columns_from_mask(winning)

    def _switch_player(self) -> None:
        self.current_player = self.other_player

    def _get_columns_from_mask(self, mask: int) -> list[int]:
        """Return the column indices represented by the mask."""
        cols = []

        while mask:
            bit = mask & -mask
            col = (bit.bit_length() - 1) // BITS_PER_COL
            cols.append(col)
            mask ^= bit
        return cols

    def _get_possible_move_mask(self) -> int:
        return (BOTTOM_MASK + self.board_mask) & ~TOP_MASK
