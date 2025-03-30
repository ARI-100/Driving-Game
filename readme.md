# 2D Drift Game

## Overview
2D Drift Game is an exciting arcade-style racing game where players control a car, navigate through obstacles, and collect power-ups. The game features increasing difficulty as players progress, making it a fun and challenging experience.

## Features
- **Dynamic Difficulty**: The game becomes progressively harder as the player survives longer, with increasing obstacle speed and frequency.
- **Power-ups**: Collect power-ups that grant temporary speed boosts or invincibility.
- **Score System**: Earn points by avoiding obstacles and collecting items.
- **Visible Timers**: Keep track of the elapsed game time and remaining power-up durations.

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Clone the repository or download the source code.
2. Ensure you have Python 3.x installed on your machine.
3. Install the Pygame library if you haven't already:
   ```bash
   pip install pygame
   ```
4. Place the required image files in the same directory as the script:
   - `city_background.png` (Background image)
   - `car_image.png` (Player car image)
   - `obstacle_car_image1.png` (First obstacle car image)
   - `obstacle_car_image2.png` (Second obstacle car image)
   - `obstacle_car_image3.png` (Third obstacle car image)

## How to Play
1. Run the game by executing the Python script:
   ```bash
   python drift_game.py
   ```
2. Use the **left** and **right arrow keys** to control the car's movement.
3. Avoid obstacles that fall from the top of the screen.
4. Collect power-ups to gain temporary advantages:
   - **Speed Boost**: Increases your speed for a short duration.
   - **Invincibility**: Makes you immune to obstacles for a limited time.
5. The game ends when you collide with an obstacle. Press **R** to restart the game.

## Controls
- **Left Arrow**: Move the car left.
- **Right Arrow**: Move the car right.
- **R**: Restart the game after a collision.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## Acknowledgments
- Thanks to the Pygame community for providing the tools and resources to create this game.
