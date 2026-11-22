"""AI opponent implementation using negamax and alpha-beta pruning."""

from dataclasses import dataclass
from connect_four.board import ConnectFour
from connect_four.constants import (
    MOVE_ORDER,
    DEPTH,
    ALPHA_BETA,
    CENTRE_MASK,
    WIN_MOVE_WEIGHT,
    OPP_WIN_MOVE_WEIGHT,
    CENTRE_WEIGHT,
    NUM_COLS,
)


@dataclass
class SearchFrame:
    """Stores the state of a node in the AI search tree."""

    move: int | None
    phase: int
    depth: int
    value: float
    index: int
    alpha: float
    beta: float
    move_list: list[int]


class ConnectFourAI:
    """Selects moves for the computer player using game-tree search."""

    def __init__(self, depth=8):
        self.depth = depth

    def suggest_move(self, game: ConnectFour, depth=DEPTH) -> int:
        """Return the recommended move"""
        if game is None:
            raise ValueError("No game found")
        if depth < 1:
            raise ValueError("Search depth must be positive")

        candidate_moves = self._candidate_moves(game)
        if len(candidate_moves) == 1:
            return candidate_moves[0]
        best_move, _ = self._negamax_ab(game)
        assert best_move is not None, "No valid move found"
        assert 0 <= best_move <= NUM_COLS, "Suggested move out of range"
        return best_move

    def _candidate_moves(self, game: ConnectFour) -> list[int]:
        """Return winning and non-losing moves if possible."""
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return []

        winning_move = game.get_winning_moves(game.player_mask)
        if winning_move:
            # Return only one winning move.
            return winning_move[0:1]

        opponent_wins = game.get_winning_moves(game.other_player_mask)

        if opponent_wins:
            # Return only one blocking move.
            return opponent_wins[0:1]
        return legal_moves

    def _board_score(self, game: ConnectFour) -> int:
        """Return the heuristic evaluation of the current board state."""
        score = 0
        # Reward centre control and penalise opponent control.
        score += CENTRE_WEIGHT * (
            (game.player_mask & CENTRE_MASK).bit_count()
            - (game.other_player_mask & CENTRE_MASK).bit_count()
        )

        # Reward imediate winning opportunities
        score += WIN_MOVE_WEIGHT * game.get_winning_mask(game.player_mask).bit_count()

        # Penalise imediate winning opportunities
        score -= (
            OPP_WIN_MOVE_WEIGHT
            * game.get_winning_mask(game.other_player_mask).bit_count()
        )

        return score

    def _negamax_ab(
        self,
        game: ConnectFour,
        depth: int = DEPTH,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
        alpha_beta: bool = ALPHA_BETA,
    ) -> tuple[int | None, float]:
        """Search the game tree using negamax with alpha-beta pruning."""
        if game.is_draw():
            return None, 0
        stack = [
            SearchFrame(
                move=None,
                phase=0,
                depth=depth,
                value=-float("inf"),
                index=0,
                alpha=alpha,
                beta=beta,
                move_list=[],
            )
        ]
        last_value = float("-inf")
        best_move = None

        while len(stack) > 0:
            current = stack[-1]

            # Traverse down the game tree
            if current.phase == 0:

                if current.move is not None:
                    game.make_move(current.move)

                # Check for terminal node.
                is_terminal = True
                if game.has_won(game.other_player_mask):
                    last_value = -(100000 + current.depth)
                elif game.is_draw():
                    last_value = 0
                elif current.depth == 0:
                    last_value = self._board_score(game)
                else:
                    # Get non-losing moves sorted by move order.
                    current.move_list = sorted(
                        self._candidate_moves(game), key=MOVE_ORDER.index
                    )
                    is_terminal = False

                # Backtrack to the parent position.
                if is_terminal:
                    if current.move is not None:
                        game.unmove()
                    stack.pop()
                    continue
                current.phase = 1

            # Process children and backtrack.
            else:
                index = current.index
                # If at least one child has been explored, update value of the current node.
                if index > 0:
                    # Negate the score to switch perspectives between players.
                    child_value = -last_value
                    if child_value > current.value:
                        current.value = child_value
                        # Update best move if at root
                        if len(stack) == 1:
                            best_move = current.move_list[index - 1]

                    # Alpha-beta pruning
                    if alpha_beta:
                        current.alpha = max(current.alpha, current.value)
                        # Prune the remaining moves when this branch cannot improve the current result.
                        if current.alpha >= current.beta:
                            last_value = current.value
                            if current.move is not None:
                                game.unmove()
                            stack.pop()
                            continue

                # If all of children have been processed, backtrack.
                if index >= len(current.move_list):
                    last_value = current.value
                    if current.move is not None:
                        game.unmove()
                    stack.pop()
                    continue

                # Pick the next child to explore.
                next_move = current.move_list[index]
                current.index += 1

                assert current.alpha <= current.beta
                stack.append(
                    SearchFrame(
                        move=next_move,
                        phase=0,
                        depth=current.depth - 1,
                        value=float("-inf"),
                        index=0,
                        alpha=-current.beta,
                        beta=-current.alpha,
                        move_list=[],
                    )
                )
        return best_move, last_value
