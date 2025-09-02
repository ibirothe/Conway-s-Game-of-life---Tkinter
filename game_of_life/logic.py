from typing import List

from game_of_life.utils import count_neighbors, create_empty_grid, random_grid

# Conway's rules
SURVIVE_NEIGHBORS = {2, 3}  # Live cell survives with 2 or 3 neighbors
BIRTH_NEIGHBORS = {3}  # Dead cell becomes alive with exactly 3 neighbors


class GameOfLife:
    """Core logic for Conway's Game of Life."""

    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.living: bool = False
        self.generation: int = 0
        self.grid: List[List[int]] = create_empty_grid(width, height)

    # -------------------------------
    # Grid manipulation
    # -------------------------------

    def reset_board(self) -> None:
        """Clear the board and reset generation counter."""
        self.grid = create_empty_grid(self.width, self.height)
        self.generation = 0

    def toggle_living(self) -> None:
        """Start or stop automatic evolution."""
        self.living = not self.living

    def touch_tile(self, x: int, y: int) -> None:
        """Toggle a cell between alive (1) and dead (0)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1 - self.grid[y][x]

    def set_cell(self, x: int, y: int, state: int) -> None:
        """Set a specific cell to 0 (dead) or 1 (alive)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = state

    def is_alive(self, x: int, y: int) -> bool:
        """Return True if the specified cell is alive."""
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] == 1

    # -------------------------------
    # Game logic
    # -------------------------------

    def update_map(self) -> None:
        """Advance the grid by one generation using Conway's rules."""
        new_grid: List[List[int]] = create_empty_grid(self.width, self.height)

        for y in range(self.height):
            for x in range(self.width):
                neighbors = count_neighbors(self.grid, x, y)
                if self.grid[y][x] == 1 and neighbors in SURVIVE_NEIGHBORS:
                    new_grid[y][x] = 1
                elif self.grid[y][x] == 0 and neighbors in BIRTH_NEIGHBORS:
                    new_grid[y][x] = 1
                # else remains 0

        self.grid = new_grid
        self.generation += 1

    def randomize_map(self) -> None:
        """Fill the grid randomly with alive and dead cells."""
        self.grid = random_grid(self.width, self.height)
        self.generation = 0

    def count_living(self) -> int:
        """Return the number of living cells on the grid."""
        return sum(sum(row) for row in self.grid)
