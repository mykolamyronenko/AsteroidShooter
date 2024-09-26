import pygame, sys
from random import randint
from ship import Ship
from laser import Laser
from asteroid import Asteroid
from score import Score
from utils import WINDOW_WIDTH, WINDOW_HEIGHT

# Basic setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroid Shooter')
clock = pygame.time.Clock()
background_surface = pygame.image.load('assets\\graphics\\background.jpg').convert()

# Sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.GroupSingle()
asteroid_group = pygame.sprite.Group()

# Score
score = Score(display_surface)

# Sprite creation
ship = Ship(spaceship_group, laser_group, asteroid_group, display_surface, score)

# asteroid timer
asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 500)

bg_music = pygame.mixer.Sound('assets\\sound\\spacemusic.wav')
bg_music.play(loops=-1)

# Game loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == asteroid_timer:
            asteroid_y_pos = randint(-150, -50)
            asteroid_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Asteroid((asteroid_x_pos, asteroid_y_pos), asteroid_group, display_surface)

    # Delta time
    dt = clock.tick() / 1000

    # Background
    display_surface.blit(background_surface, (0, 0))

    # Update
    spaceship_group.update(dt)
    laser_group.update(dt)
    asteroid_group.update(dt)

    score.display()

    # Graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    asteroid_group.draw(display_surface)

    # Draw the frame
    pygame.display.update()
