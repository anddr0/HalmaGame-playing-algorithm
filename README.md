# HalmaGame and alpha-beta

This repository contains a Python project for simulating and managing the state of a board game, specifically Halma. The project includes various scripts to initialize the game board, manage game states, and provide utility functions for the game logic.

## Project Overview

This project is focused on simulating and managing the Halma game state and making decisions with alpha-beta (min-max) algorithm to perform best moves. Halma is a strategy board game involving movement of pieces across a board, and this project provides a framework to handle game initialization, state management, and game rules.

## Repository Structure

- **GameState.py**: The main script that manages the game state and handles the core game logic.
- **HalmaGame.py**: Contains the logic specific to the Halma game, including rules and game flow.
- **initial_board.txt**: A text file that specifies the initial configuration of the game board.
- **vars.py**: Defines variables and utility functions that are used across the project for managing game states and operations.

## How the Project Works

### GameState.py

This script is the heart of the project and is responsible for managing the state of the game. It tracks the positions of pieces, validates moves, and updates the game state as the game progresses.

Key functionalities include:
- **Initialize Game State**: Reads the initial configuration from `initial_board.txt` and sets up the board.
- **Validate Moves**: Checks if a move is valid based on the game rules defined in `HalmaGame.py`.
- **Update State**: Updates the game state after each valid move, ensuring that the game progresses correctly.

Example usage:
```python
from GameState import GameState

game = GameState()
game.initialize()
game.make_move(player, move)
game.display_board()
```

### HalmaGame.py

This script contains the logic specific to the Halma game, including the rules for moving pieces and determining valid moves.

Key functionalities include:
- **Game Rules**: Implements the rules of Halma, such as move restrictions and capturing logic.
- **Move Generation**: Provides methods to generate all possible moves for a given game state.

Example usage:
```python
from HalmaGame import HalmaGame

halma = HalmaGame()
valid_moves = halma.get_valid_moves(player, current_state)
```

### initial_board.txt

A text file that defines the initial setups (espetiatly for testing) of the game board. Each line represents a row on the board, and each character in the line represents a cell, which could be empty or occupied by a piece.

Example format:
```
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
```

### vars.py

Contains utility functions and constants that are used across the project. This script helps to keep the code organized and maintain consistent values for variables used in game logic.

Key functionalities include:
- **Constants**: Defines constants such as board size, piece symbols, etc.
- **Utility Functions**: Provides helper functions for tasks like coordinate conversions and state checks.

Example usage:
```python
from vars import BOARD_SIZE, EMPTY_CELL

print(f"Board size is {BOARD_SIZE}")
```
