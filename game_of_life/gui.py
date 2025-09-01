import tkinter as tk
from tkinter import ttk
from .logic import GameOfLife

CELL_SIZE = 20
UPDATE_RATE_MS = 200

class GameOfLifeApp(tk.Tk):
    """Tkinter GUI for Conway's Game of Life."""

    def __init__(self, game: GameOfLife) -> None:
        super().__init__()
        self.title("Game of Life")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")
        self.game = game

        # Style
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#d0d0d0")
        style.configure("TButton",
                        background="#2d2d2d",
                        foreground="#ffffff",
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor="none",
                        padding=6)
        style.map("TButton", background=[("active", "#3a3a3a")])

        # Canvas
        self.canvas_width = game.width * CELL_SIZE
        self.canvas_height = game.height * CELL_SIZE
        self.canvas = tk.Canvas(self, width=self.canvas_width,
                                height=self.canvas_height, bg="#0e0e0e",
                                highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        # Controls
        controls = ttk.Frame(self)
        controls.pack(fill="x", pady=5)
        self.play_button = ttk.Button(controls, text="▶ Play", command=self.toggle_play)
        self.play_button.pack(side="left", padx=5)
        ttk.Button(controls, text="⟲ Clear", command=self.clear_board).pack(side="left", padx=5)
        ttk.Button(controls, text="➤ Step", command=self.step_board).pack(side="left", padx=5)
        ttk.Button(controls, text="✦ Randomize", command=self.randomize_board).pack(side="left", padx=5)

        # Status bar
        self.status = ttk.Label(self, text="Generation: 0 | Alive: 0", anchor="center")
        self.status.pack(fill="x", pady=(0, 8))

        # Bind mouse
        self.canvas.bind("<Button-1>", self.on_click)

        # Initialize grid
        self.rects = [[None for _ in range(game.width)] for _ in range(game.height)]
        for y in range(game.height):
            for x in range(game.width):
                x1, y1 = x * CELL_SIZE, y * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                    fill="#0e0e0e", outline="#2a2a2a")
                self.rects[y][x] = rect

        self.game.randomize_map()
        self.draw_board()
        self.toggle_play()
        self.update_loop()

    # --- Button actions ---
    def toggle_play(self) -> None:
        self.game.toggle_living()
        self.play_button.config(text="⏸ Pause" if self.game.living else "▶ Play")

    def clear_board(self) -> None:
        self.game.reset_board()
        self.draw_board()

    def step_board(self) -> None:
        self.game.update_map()
        self.draw_board()

    def randomize_board(self) -> None:
        self.game.randomize_map()
        self.draw_board()

    # --- Input ---
    def on_click(self, event) -> None:
        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
        if 0 <= x < self.game.width and 0 <= y < self.game.height:
            self.game.touch_tile(x, y)
            self.draw_board()

    # --- Rendering ---
    def draw_board(self) -> None:
        for y, row in enumerate(self.game.grid):
            for x, cell in enumerate(row):
                color = "#f5f5f5" if cell else "#0e0e0e"
                self.canvas.itemconfig(self.rects[y][x], fill=color)
        self.status.config(text=f"Generation: {self.game.generation} | Alive: {self.game.count_living()}")

    # --- Main loop ---
    def update_loop(self) -> None:
        if self.game.living:
            self.game.update_map()
            self.draw_board()
        self.after(UPDATE_RATE_MS, self.update_loop)
