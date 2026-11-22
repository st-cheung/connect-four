# Connect Four

A Connect Four game built with Python and Pygame, featuring an AI opponent.

## Features

- Player vs Player and Player vs AI game modes.

- AI opponent using negamax with alpha-beta pruning.

- Save/load functionality.

- Interactive interface with menus and pause functionality.


## Installation

**Requirements**: Python 3.11+
1. Clone the repository:
   ```bash
   git clone
   cd connect-four
2. Install dependencies:
   ```bash
   py -m pip install -r requirements.txt
3. Run the game:
   ```bash
   python main.py

## AI Implementation

The computer opponent uses negamax with alpha-beta pruning to search possible moves and select a move based on the resulting positions.

**Negamax**: Evaluates positions from the perspective of the current player, allowing the same search logic to be used for both players.

**Alpha-beta pruning**: Skips branches that cannot improve the current result, reducing the number of positions evaluated.

**Move ordering**: Searches columns from the centre outwards to prioritise strategically valuable moves.

**Evaluation function**: Scores board positions based on factors such as centre control and potential winning sequences.

**Bitboard representation**: Uses a bitboard representation for efficient board operations and win detection.