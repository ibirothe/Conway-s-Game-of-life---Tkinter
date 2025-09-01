import unittest
from typing import List
from game_of_life.logic import GameOfLife


class TestGameOfLife(unittest.TestCase):
    """Unit tests for the GameOfLife logic."""

    def setUp(self) -> None:
        self.width: int = 5
        self.height: int = 5
        self.game: GameOfLife = GameOfLife(self.width, self.height)

    def test_reset_board(self) -> None:
        """Ensure reset_board clears the map and resets generation."""
        # Fill some cells
        self.game.grid[0][0] = 1
        self.game.grid[1][1] = 1
        self.game.generation = 5
        self.game.reset_board()
        # All cells should be 0
        for row in self.game.grid:
            self.assertTrue(all(cell == 0 for cell in row))
        self.assertEqual(self.game.generation, 0)

    def test_toggle_living(self) -> None:
        """Ensure toggle_living switches the living flag."""
        self.assertFalse(self.game.living)
        self.game.toggle_living()
        self.assertTrue(self.game.living)
        self.game.toggle_living()
        self.assertFalse(self.game.living)

    def test_touch_tile(self) -> None:
        """Ensure touch_tile toggles a cell correctly."""
        self.assertEqual(self.game.grid[0][0], 0)
        self.game.touch_tile(0, 0)
        self.assertEqual(self.game.grid[0][0], 1)
        self.game.touch_tile(0, 0)
        self.assertEqual(self.game.grid[0][0], 0)

    def test_update_map_underpopulation(self) -> None:
        """Single live cell should die due to underpopulation."""
        self.game.grid[0][0] = 1
        self.game.update_map()
        self.assertEqual(self.game.grid[0][0], 0)

    def test_update_map_survival(self) -> None:
        """Live cell with 2 or 3 neighbors survives."""
        # Create a cell with 2 neighbors
        self.game.grid[0][0] = 1
        self.game.grid[0][1] = 1
        self.game.grid[1][0] = 1
        self.game.update_map()
        self.assertEqual(self.game.grid[0][0], 1)

    def test_update_map_reproduction(self) -> None:
        """Dead cell with exactly 3 neighbors becomes alive."""
        self.game.grid[0][1] = 1
        self.game.grid[1][0] = 1
        self.game.grid[1][1] = 1
        self.game.update_map()
        self.assertEqual(self.game.grid[0][0], 1)

    def test_update_map_overpopulation(self) -> None:
        """Live cell with more than 3 neighbors dies."""
        cells: List[tuple[int, int]] = [(0,0), (0,1), (1,0), (1,1), (0,2)]
        for y, x in cells:
            self.game.grid[y][x] = 1
        self.game.update_map()
        # Cell at (0,1) has 4 neighbors → dies
        self.assertEqual(self.game.grid[0][1], 0)

    def test_randomize_map(self) -> None:
        """Randomize_map should fill the board with both 0 and 1."""
        self.game.randomize_map()
        flat_map: List[int] = [cell for row in self.game.grid for cell in row]
        self.assertIn(0, flat_map)
        self.assertIn(1, flat_map)
        self.assertEqual(self.game.generation, 0)

    def test_count_living(self) -> None:
        """count_living should return correct number of live cells."""
        self.game.grid[0][0] = 1
        self.game.grid[1][1] = 1
        self.assertEqual(self.game.count_living(), 2)


if __name__ == "__main__":
    unittest.main()
