# Asteroid Shooter Game

## Overview
Asteroid Shooter is an engaging 2D game built using Pygame. The player controls a spaceship that can shoot lasers to destroy incoming asteroids. The objective is to survive as long as possible and destroy as many asteroids as possible to increase your score.


## Features
- Mouse Controls: Navigate the spaceship using the mouse.
- Laser Shooting: Shoot lasers to destroy asteroids.
- Scoring System: Earn points for each destroyed asteroid.

## Setup

### Prerequisites
- Python 3
- Pygame library

### Installation
1. Clone the repository:
    ```
    git clone https://github.com/mykolamyronenko/AsteroidShooter.git
    cd AsteroidShooter
    ```

2. Install the required dependencies:
    ```
    pip install pygame-ce
    ```
    or
    ```
    pip install -r requirements.txt
    ```

3. Ensure the following directory structure:
    ```
    asteroid-shooter/
    ├── assets/
    │   ├── graphics/
    │   │   ├── Battleplane.png
    │   │   ├── background.jpg
    │   │   ├── laser.png
    │   │   ├── asteroid.png
    │   │   └── subatomic.ttf
    │   └── sound/
    │       ├── explosion.wav
    │       ├── laser.wav
    │       └── spacemusic.wav
    ├── main.py
    ├── ship.py
    ├── laser.py
    ├── asteroid.py
    ├── alien.py
    ├── score.py
    ├── utils.py
    └── README.md

    ```

## How to Play
1. Run the game:
    ```
    python main.py
    ```

2. Control the spaceship using the mouse. The spaceship will follow the cursor.

3. Click the left mouse button to shoot lasers.

4. Destroy asteroids to increase your score. The score is displayed at the top-left corner of the screen.

5. Avoid collisions with meteors. If a meteor hits the spaceship, the game will end.

## Code Structure
- `main.py`: Contains the game loop and initialization code.
- `ship.py`: Contains the `Ship` class, which handles the spaceship's behavior.
- `laser.py`: Contains the `Laser` class, which handles the laser's behavior.
- `asteroid.py`: Contains the `Asteroid` class, which handles the asteroid's behavior.
- `alien.py`:Contains the `Alien` class, which handles the alien’s behavior.
- `score.py`: Contains the `Score` class, which handles the scoring system.
- `utils.py`: Contains utility functions and constants.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- Pygame library for making game development in Python accessible and fun.
- Sound effects and graphics from various free resources.


