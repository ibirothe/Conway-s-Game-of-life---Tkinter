from game_of_life.gui import GameOfLifeApp
from game_of_life.logic import GameOfLife

MAP_SIZE = (55, 30)


def main() -> None:
    game = GameOfLife(*MAP_SIZE)
    app = GameOfLifeApp(game)
    app.mainloop()


if __name__ == "__main__":
    main()
