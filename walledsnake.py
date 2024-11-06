import tkinter as tk
from tkinter import messagebox
import ctypes
import os
from PIL import Image, ImageDraw
from random import randint

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1040
WALLPAPER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'snake_wallpaper.png')

GRID_COLUMNS, GRID_ROWS = 32, 18
GRID_SIZE = min(DISPLAY_WIDTH // GRID_COLUMNS, DISPLAY_HEIGHT // GRID_ROWS)

GRID_START_X = (DISPLAY_WIDTH - (GRID_COLUMNS * GRID_SIZE)) // 2
GRID_START_Y = (DISPLAY_HEIGHT - (GRID_ROWS * GRID_SIZE)) // 2

DIRECTION_MAP = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

class SnakeGame:
    def __init__(self):
        self.snake = [(GRID_COLUMNS // 2, GRID_ROWS // 2)]
        self.direction = 'right'
        self.food = self.spawn_food()
        self.running = True
        self.score = 0

    def spawn_food(self):
        while True:
            food_pos = (randint(0, GRID_COLUMNS - 1), randint(0, GRID_ROWS - 1))
            if food_pos not in self.snake:
                return food_pos

    def update(self):
        if not self.running:
            return

        head_x, head_y = self.snake[0]
        dir_x, dir_y = DIRECTION_MAP[self.direction]
        new_head = (head_x + dir_x, head_y + dir_y)

        if (new_head[0] < 0 or new_head[0] >= GRID_COLUMNS or
            new_head[1] < 0 or new_head[1] >= GRID_ROWS or
            new_head in self.snake):
            messagebox.showinfo("Game Over", f"You lose! Final score: {self.score}")
            self.running = False
            return

        self.snake = [new_head] + self.snake
        if new_head == self.food:
            self.food = self.spawn_food()
            self.score += 1
        else:
            self.snake.pop()

    def change_direction(self, new_direction):
        if (self.direction == 'up' and new_direction != 'down' or
            self.direction == 'down' and new_direction != 'up' or
            self.direction == 'left' and new_direction != 'right' or
            self.direction == 'right' and new_direction != 'left'):
            self.direction = new_direction

    def draw(self):
        image = Image.new('RGB', (DISPLAY_WIDTH, DISPLAY_HEIGHT), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        for x, y in self.snake:
            top_left = (GRID_START_X + x * GRID_SIZE, GRID_START_Y + y * GRID_SIZE)
            bottom_right = (top_left[0] + GRID_SIZE, top_left[1] + GRID_SIZE)
            draw.rectangle([top_left, bottom_right], fill=(128, 128, 128))
            draw.rectangle([top_left[0] + 2, top_left[1] + 2, bottom_right[0] - 2, bottom_right[1] - 2], fill=(0, 255, 0))

        fx, fy = self.food
        food_top_left = (GRID_START_X + fx * GRID_SIZE, GRID_START_Y + fy * GRID_SIZE)
        food_bottom_right = (food_top_left[0] + GRID_SIZE, food_top_left[1] + GRID_SIZE)
        draw.rectangle([food_top_left, food_bottom_right], fill=(255, 0, 0))

        image.save(WALLPAPER_PATH, format='PNG')
        self.set_wallpaper(WALLPAPER_PATH)

    def set_wallpaper(self, path):
        if os.name == 'nt':
            SPI_SETDESKWALLPAPER = 20
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDCHANGE = 0x02
            result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
            if not result:
                print("Failed to set wallpaper")
            else:
                print("Wallpaper set successfully")

game = SnakeGame()

def create_controls():
    global root, retry_button, score_label
    root = tk.Tk()
    root.title("WinSnake")
    
    font = ('Arial', 15)

    tk.Button(root, text="←", command=lambda: game.change_direction('left'), font=font, width=3, height=1).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(root, text="↑", command=lambda: game.change_direction('up'), font=font, width=3, height=1).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="↓", command=lambda: game.change_direction('down'), font=font, width=3, height=1).grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="→", command=lambda: game.change_direction('right'), font=font, width=3, height=1).grid(row=1, column=2, padx=10, pady=10)

    retry_button = tk.Button(root, text="⟳", command=retry_game, font=font, width=3, height=1)
    retry_button.grid(row=3, column=1, pady=10)
    retry_button.grid_remove()

    score_label = tk.Label(root, text="Score: 0", font=('Arial', 15))
    score_label.grid(row=4, column=1, pady=10)
    score_label.grid_remove()

    root.bind("<Left>", lambda event: game.change_direction('left'))
    root.bind("<Up>", lambda event: game.change_direction('up'))
    root.bind("<Down>", lambda event: game.change_direction('down'))
    root.bind("<Right>", lambda event: game.change_direction('right'))
    
    root.after(100, game_loop)
    
    root.deiconify()

    root.mainloop()

def game_loop():
    game.update()
    game.draw()
    if game.running:
        root.after(200, game_loop)
    else:
        retry_button.grid()
        score_label.config(text=f"Score: {game.score}")
        score_label.grid()

def retry_game():
    game.__init__()
    retry_button.grid_remove()
    score_label.grid_remove()
    game_loop()

create_controls()
