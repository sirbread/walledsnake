# walledsnake

**WINDOWS ONLY. Sorry to my Linux users!** Walled snake, to put it very simply, is snake, but your desktop wallpaper is the game. 
Uses the Tkinter and Pillow library to generate the game grid and set the wallpaper.

## Instructions

1. **Start the Game:**
   - Simply run `walledsnake.py` to start the game.
   - The control window should pop up automatically.
   - Minimize everything (win + d) once you hit run to see the wallpaper, or your game. Then, bring up the tkinter window.
   - **NOTICE:** Your wallpaper **will get overwritten,** so be careful and download a copy of your wallpaper if you want to keep it. 

2. **Gameplay:**
   - Use the arrow buttons in the control window to move the snake OR keyboard keys:
     - **Left Arrow (←)**: Move the snake left.
     - **Up Arrow (↑)**: Move the snake up.
     - **Down Arrow (↓)**: Move the snake down.
     - **Right Arrow (→)**: Move the snake right.
   - The game will generate food (red squares) on the grid.
   - The snake (green squares) grows longer as it eats food.
   - The game ends if the snake hits the boundaries of the grid (16:9 scaled) or itself.

3. **Score:**
   - Your score will increase each time the snake eats the "red square" (apple).
   - The score is displayed at the bottom of the control window after you lose.
   - If the game ends, click the **Retry** button (⟳) to start a new game.

## Requirements
- Python 3.x
- Pillow==9.5.0
- Tkinter


