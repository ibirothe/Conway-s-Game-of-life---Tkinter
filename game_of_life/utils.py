import os
import random
from typing import List

# -------------------------------
# Grid Utilities
# -------------------------------


def create_empty_grid(width: int, height: int) -> List[List[int]]:
    """
    Create an empty grid of given width and height.
    All cells initialized to 0 (dead).
    """
    return [[0 for _ in range(width)] for _ in range(height)]


def random_grid(width: int, height: int) -> List[List[int]]:
    """
    Create a grid randomly filled with 0 (dead) or 1 (alive) cells.
    """
    return [[random.choice([0, 1]) for _ in range(width)] for _ in range(height)]


def count_neighbors(grid: List[List[int]], x: int, y: int) -> int:
    """
    Count the number of alive neighbors for a cell at position (x, y).
    Grid wraps around edges (toroidal).
    """
    height: int = len(grid)
    width: int = len(grid[0])
    directions: List[tuple[int, int]] = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]
    return sum(grid[(y + dy) % height][(x + dx) % width] for dx, dy in directions)


# -------------------------------
# Pattern Utilities
# -------------------------------


def load_pattern(filename: str) -> List[List[int]]:
    """
    Load a pattern from a text file.
    Each line should be a row of 0s and 1s, e.g.:
    010
    001
    111
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Pattern file not found: {filename}")

    with open(filename, "r") as f:
        grid: List[List[int]] = []
        for line in f:
            line = line.strip()
            if line:
                grid.append([int(c) for c in line])
    return grid


def apply_pattern(
    grid: List[List[int]], pattern: List[List[int]], top: int = 0, left: int = 0
) -> None:
    """
    Apply a smaller pattern onto an existing grid at position (top, left).
    Modifies the grid in-place.
    """
    height: int = len(grid)
    width: int = len(grid[0])
    for y, row in enumerate(pattern):
        for x, cell in enumerate(row):
            if 0 <= top + y < height and 0 <= left + x < width:
                grid[top + y][left + x] = cell
