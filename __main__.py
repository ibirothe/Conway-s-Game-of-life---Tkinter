from game_of_life.logic import GameOfLife
from game_of_life.gui import GameOfLifeApp

MAP_SIZE = (55, 30)

def main() -> None:
    game = GameOfLife(*MAP_SIZE)
    app = GameOfLifeApp(game)
    app.mainloop()

if __name__ == "__main__":
    main()
